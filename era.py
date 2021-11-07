import streamlit as st
import pandas as pd
import datetime

#write todays date
today = datetime.date.today()

st.text_input("Your experiment ID", key="ELN_ID")

# You can access the value at any point with:
st.session_state.ELN_ID

st.text('please consider greener solvents')

def overall_risk_statement(risk,hazard):
    if risk == 'HIGH' and hazard == 'HIGH':
        return ('overall risk is high')
    elif risk == 'LOW' and hazard == 'LOW':
        return('overall risk is low and generic risk assement covers all')
    elif risk == 'MEDIUM' or 'HIGH' and hazard == 'MEDIUM' or 'HIGH':
        return('overall risk is high and additional control measures reduced the risk to acceptable')

def room_temp(reaction_temp):
    if reaction_temp <= 30 or reaction_temp > 15:
        return('reaction was conducted at room temperature')
    else:
        return(f'reaction was conducted at {reaction_temp}')

def volumn_of_gas(gas_mmol,temp,gas):
    n_ideal_gas=(float(gas_mmol)/1000)
    temp_ideal_gas= float(temp) + 273
    Volume = ((n_ideal_gas*8.31441*temp_ideal_gas)/101325)*1E6
    return(f'{Volume} mL of {gas} is generated at {temp} C and 1 ATM')

option3 = st.selectbox('WHAT SCALE IS THE REACTION CONDUCTED ON', ['', 'SMALL < 10 mmol', 'LARGE > 100 mmol'])

reaction_temp = st.number_input("What temperature will you be conducting the experiment at", step=1)

st.write('Select all box that apply to your reaction:')
option_x = st.checkbox('reaction is exothermic')
option_y = st.checkbox('incompatibilities exist between reaction compotents')
option_z = st.checkbox('pyrophroic reagent are used')
option_a = st.checkbox('strong oxidising agents are used')
risk_gas = st.checkbox('gas evolution is expected during the reaction or workup')

rxn_hazard = st.selectbox(
    'What is the REACTION HAZARD?',
     ['','HIGH','MEDIUM','LOW'])

option2 = st.selectbox(
    'What is the REACTION RISK?',
     ['','HIGH','MEDIUM','LOW'])

option4 = st.selectbox(
    'Potential thermal instability and explosibility of intermediates, products and reaction mixtures',
    ['Yes','No'])

if risk_gas == True:
    risk_what_gas = st.number_input("How many mmol of gas is expected", step=1.,format="%.2f")

'Reaction was started on ',today, room_temp(reaction_temp),'Reaction hazard is ', rxn_hazard, ' and risk is', option2, 'the reaction is conducted on a', option3, overall_risk_statement(rxn_hazard,option2)

