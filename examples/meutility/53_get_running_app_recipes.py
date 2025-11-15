import os
import pandas as pd
import pprint

from pymeu import MEUtility
from pymeu import comms
from pymeu import me

'''
NOTE - Typically only the main MEUtility functions are intended
to be exposed for use.  Other functions (in this case from comms and
me) can allow for other interesting code to be written, but are more
likely to have breaking changes over time.

This example finds the Startup *.MER file on the remote terminal,
uploads it in memory, and extracts the RecipePlus data.

It also includes an example of casting the returned data into a Pandas
dataframe for easier manipulation, saving to CSV, etc.
'''

def recipeplus_to_dataframe(recipe_file: me.types.MERecipePlusFile) -> pd.DataFrame:
    data = {
        "name": [ingred.name for ingred in recipe_file.ingredients],
        "type": [ingred.type for ingred in recipe_file.ingredients],
        "min": [ingred.min for ingred in recipe_file.ingredients],
        "max": [ingred.max for ingred in recipe_file.ingredients],
        "decimal_places": recipe_file.decimal_places
    }

    for ds in recipe_file.data_sets:
        data[ds.name] = ds.value

    for ts in recipe_file.tag_sets:
        data[ts.name] = ts.value

    df = pd.DataFrame(data)
    return df

meu = MEUtility(comms_path='YourTerminalIpAddress')
info = meu.get_terminal_info()
with comms.Driver(comms_path=meu.comms_path) as cip:
    device = me.validation.get_terminal_info(cip)
    mer = me.transfer.upload(
        cip=cip,
        device=device,
        file_path_terminal=f'{device.me_paths.runtime}\\{info.device.startup_mer_file}',
        progress=None
    )
    result = me.application.recipeplus_deserialize(
        input_path=bytes(mer),
        progress=None
    )

    # Example output for raw DataClass
    pprint.pprint(result)

    # Example output for pandas dataframe
    for x in result:
        df = recipeplus_to_dataframe(x)
        print(df)