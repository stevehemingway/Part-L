"""
Thermal conductivity (lambda) values for common building materials.
Units: W/mK
"""

import pint

ureg = pint.UnitRegistry()

LAMBDA = {
    # Insulation
    "xps": 0.04,  # Polyisocyanurate
    # Masonry
    "brick": 0.9,  # Medium density clay brick (~1800 kg/m³)
    "clay_brick_lightweight": 0.5,  # Lightweight clay brick (< 1700 kg/m³)
    # Board materials
    "plasterboard": 0.25,  # Standard plasterboard (gypsum)
}

# Example wall construction with thicknesses in mm
WALL = {
    "plasterboard": 13.0,  # Internal plaster finish
    "brick": 220.0,  # Main structural brick layer
    "xps": 50.0,  # internal insulation board
}


def R_value(element):
    return (WALL[element] / 1000) / LAMBDA[element]


def lambda_val(material):
    return LAMBDA[material] * ureg.watts / (ureg.meter * ureg.kelvin)


tot_R = 0.0

for i in WALL:
    print(i)
    R = R_value(i)
    tot_R += R
    print("R value: {:.5f}".format(R))

print("total R: {:.5f}".format(tot_R))

print("U-value for wall is {:.3f}".format(1.0 / tot_R))

EWI_thickness = 60 / 1000 * ureg.meter  # in m. as per Jostec SAP

brick_thickness = (0.220 + 0.025) * ureg.meter  # add about an inch for solid plaster
print("payback for EWI, :")

r_brick = brick_thickness / lambda_val("brick")
print("R for brick, {}".format(r_brick))
print("U for brick: {}".format(1.0 / r_brick))

r_xps = EWI_thickness / lambda_val("xps")
print("R for xps, {}".format(r_xps))
print("U for xps: {}".format(1.0 / r_xps))


r_with_ewi = r_brick + r_xps


ureg.define("gbp = []")

wall = []

degree_days = 2250 * ureg.kelvin  # assumed, base 15C,  for Knebworth.

# cost psm with brick:
# gas_price_bill = 0.0574  # pounds/kWh
gas_price_bill = 0.03  # pounds/kWh

gas_price = (
    gas_price_bill / 1000 / (60 * 60) / (ureg.watt * ureg.second) * ureg.gbp
)  # pounds/J


day = 24 * 60 * 60 * ureg.seconds

u_delta = 1.0 / r_brick - 1.0 / r_with_ewi

print("change in u value from EWI {}".format(u_delta))

print("energy psm per degree per day {}".format(u_delta))
print(
    "incremental saving psm for brick alone for one degree day: {}".format(
        day * gas_price * u_delta
    )
)

year_cost_psm = degree_days * day * gas_price * u_delta

print("cost saving psm for ewi alone for one year: {}".format(year_cost_psm))

installation_cost = 200 * ureg.gbp / (ureg.meter**2)  # pounds

# based on non-binding verbal quote from TAW of £30K for front and side elevations, ~150m^2 of solid wall.

print("simple payback {}".format(installation_cost / year_cost_psm))
