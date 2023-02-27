from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


app = Dash(external_stylesheets=[dbc.themes.COSMO])
server=app.server
rxn_temp = dcc.Input(value='', type='number',placeholder='temperature',max=300)
my_output = html.Div()
vial_vol = dcc.Input(value='', type='number',placeholder='vial vol',min=1,max=50)
gas_mmol = dcc.Input(value='0',type='number',placeholder='mmol gas',min=0)
vol_solvent = dcc.Input(value='',type='number')
#need a way of error proofing vol_solvent < vial_vol (child dependency?)

def calculate_pressure(vial_vol,vol_solvent,rxn_temp,mmol_gas_generated):
    total_gas = float(vial_vol) - float(vol_solvent)
    mmol_gas = (total_gas/24.5) + float(mmol_gas_generated)
    temp_ideal_gas= float(rxn_temp) + 273
    print(mmol_gas)
    pressure = (mmol_gas/1000)*8.314*(temp_ideal_gas)/(total_gas/1E6)
    return round(pressure/100000, 2)

app.layout = html.Div([
    html.H1("Sealed vessel risk assesment tool"),
    html.Div([
        "Reaction temp: ",
        rxn_temp, 
    ],style={'padding': 10, 'flex': 1}),
    html.Br(),
    html.Div(["Volume of vial (mL): ",vial_vol],style={'padding': 10, 'flex': 1}),
    html.Br(),
    html.Div(["mmol of gas generated in reaction: ",gas_mmol],style={'padding': 10, 'flex': 1}),
    html.Br(),
    html.Div(["total volume of solvent used (mL): ",vol_solvent],style={'padding': 10, 'flex': 1}),
    html.Br(),
    html.Div(),
    html.Button('Run', id='apply-button', n_clicks=0),
    my_output
])

if rxn_temp != None:
    @callback(
        Output(my_output, component_property='children'),
        [Input('apply-button','n_clicks')],
        Input(vial_vol, component_property='value'),
        Input(vol_solvent,component_property='value'),
        Input(rxn_temp,component_property='value'),
        Input(gas_mmol,component_property='value')
    )
    def update_output_div(n_clicks,vial_vol,vol_solvent,rxn_temp,gas_mmol):
        if n_clicks > 0:
            delta_vol = calculate_pressure(vial_vol,vol_solvent,rxn_temp,gas_mmol)
            n_clicks = 0
            if delta_vol < 7:
                return f'The reaction was conducted in vial of volume {vial_vol} mL, with total solvent volume of {vol_solvent} mL at a max reaction temperature of {rxn_temp}, this generates a pressure of {delta_vol} bar, assuming ideal gas and no vapor pressure'
            else:
                return f'pressure is {delta_vol} bar, recommended that the maximum operating pressure be no more than 100 psi (~7 bar). '
        else:
            return 'not calaculated yet'

if __name__ == '__main__':
    app.run_server(debug=True)
