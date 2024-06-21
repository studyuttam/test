import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_shadcn_ui as ui
import uk_map


#import excel file name disabilitycensus2021.xlsx sheet name Table 6

df = pd.read_excel('Data/disabilitycensus2021.xlsx', sheet_name='Table 6')

st.title('Quantitative Analysis')


tab1, tab2, tab3, tab4 = st.tabs(['Census 2021', 'SEN Dashboard', 'Employment', 'Education'])
with tab1:
  st.header('Census 2021')
  # Create two columns for the multiselects
  col1, col2 = st.columns(2)

  # Place each multiselect in one column
  with col1:
    local_authority = st.multiselect('Local Authority', df['Local Authority'].unique(), default=['Brent'])
  with col2:
    age_group = st.multiselect('Age Group', df['Age'].unique(), default=['15 to 19'])


  #write code if nothing is selected for local_authority and age_group then display a message to select local_authority and age_group for the data to be displayed
  if len(local_authority) == 0 or len(age_group) == 0:
      st.write('Please select Local Authority and Age Group')
  else:

    #display the selected local authority and age group
    st.write('Local Authority:', local_authority)
    st.write('Age Group:', age_group)


    #st_card('Completed Orders', value=76.4, show_progress=True)

    #display df['Count'] for selected local authority and age group in card

    #filter the data based on the selected local authority and age group
    disabled_population = df[(df['Local Authority'].isin(local_authority))
                        & (df['Age'].isin(age_group))
                        & (df['Category'] == 'Four category')
                        & (df['Sex'].isin(['Male','Female']))
                        & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]

    st.write('Disabled Population:', disabled_population['Count'].sum())

    # Total population

    total_population = df[(df['Local Authority'].isin(local_authority))
                        & (df['Age'].isin(age_group))
                        & (df['Category'] == 'Four category')
                        & (df['Sex'].isin(['Male','Female']))
                        & (df['Disability Status'].isin(['Disabled; limited a lot']))]

    st.write('Total Population:', total_population['Population'].sum())

    #Total Population and Disabled Population in a card
    cols = st.columns(2)
    with cols[0]:
      ui.metric_card(title="Total Population", content=total_population['Population'].sum(), description=" ", key="card1")
    with cols[1]:
      ui.metric_card(title="Disabled Population", content=disabled_population['Count'].sum(), description=" ", key="card2")
    
    
    # Create a figure for 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(25, 20)) 

    #display total population and disabled population in bar chart
    
    sns.barplot(x=['Total Population', 'Disabled Population'], y=[total_population['Population'].sum(), disabled_population['Count'].sum()], ax=axs[0, 0])
    axs[0,0].set_title('Total Population vs Disabled Population')
    

    # Plot 2: Disabled Population by Sex

    #display a pie chart for different sex in the disabled
    
    disabled_population.groupby('Sex')['Count'].sum().plot.pie(autopct='%1.1f%%', ax=axs[0, 1])
    axs[0, 1].set_title('Disabled Population by Sex')
    
    # Plot 3: Population Group by Disability Status
    st.write('Disabled Population:', disabled_population.groupby('Sex')['Count'].sum())
    poulation_grpby_category = df[(df['Local Authority'].isin(local_authority))
                        & (df['Age'].isin(age_group))
                        & (df['Category'] == 'Four category')
                        & (df['Sex'].isin(['Male','Female']))
                        ]

    # Prepare data for seaborn
    data = poulation_grpby_category.groupby('Disability Status')['Count'].sum().reset_index()

    # Create a bar plot
    
    barplot = sns.barplot(x='Disability Status', y='Count', data=data, palette='viridis',ax=axs[1, 0])

    # Add data labels
    for bar in barplot.patches:
        barplot.text(x = bar.get_x() + bar.get_width() / 2, 
                    y = bar.get_height(), 
                    s = f'{int(bar.get_height())}', 
                    ha = 'center', 
                    va = 'bottom')

    # Set y-axis limit
    axs[1,0].set_ylim(0, data['Count'].max() * 1.1)

    axs[1, 0].tick_params(axis='x', rotation=45)
    axs[1, 0].set_title('Population Group by Disability Status', fontsize=16, fontweight='bold', y=1.05)
    
    # Since there's no fourth plot specified, you can hide the fourth subplot or use it for another plot
    axs[1, 1].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Display the figure in Streamlit
    st.pyplot(fig)

    #display disabled population of Top 10 local authorities in a bar chart

    # Convert 'Count' column to numeric
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    uk_disabled_population = df[(df['Age'].isin(age_group))
                        & (df['Category'] == 'Four category')
                        & (df['Sex'].isin(['Male','Female']))
                        & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]

    # Get the top 10 local authorities by disabled population
    disabled_population_top10 = uk_disabled_population.groupby('Local Authority')['Count'].sum().nlargest(10)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=disabled_population_top10.index, y=disabled_population_top10.values)
    plt.xticks(rotation=45)
    plt.title('Disabled Population For Top 10 Local Authority')
    st.pyplot(plt)


    #UK Map
    st.map()

with tab2:
  st.header('SEN Dashboard')
  st.write('Coming Soon')

with tab3:
  st.header('Employment')
  st.write('Coming Soon')

with tab4:
  st.header('Education')
  st.write('Coming Soon')

