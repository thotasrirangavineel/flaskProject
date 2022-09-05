# import needed libraries
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import exists as file_exists

# creating flask object
app = Flask(__name__)


# creating flask page and declaring methods used
@app.route('/', methods=['GET', 'POST'])
def mainbody():
    # read csv file with data
    nfa = pd.read_csv('NFA 2018.csv')

    # CLean and process data
    for each in nfa:
        if type(nfa[each][0]) != str:
            mv = nfa[each].mean()
            nfa[each].fillna(mv)
            nfa[each].replace(to_replace=np.NaN, value=nfa[each].mean(), inplace=True)

    # collect unique values to display in dropdown
    country = nfa.country.unique()
    record = nfa.record.unique()

    # get the variables from frontend using POST procedure
    country_select = request.form.get('country')
    record_select = request.form.get('record')

    # plot graph for several mentioned lands
    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='grazing_land', color='blue')

    plt.title('year vs grazing_land')
    # save plot as image to render on html page
    plt.savefig('yvsgl.png')

    # move file to the static subfolder to follow flask protocol
    if file_exists('static/yvsgl.png'):
        os.replace('yvsgl.png', 'static/yvsgl.png')
    else:
        os.rename('yvsgl.png', 'static/yvsgl.png')

    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='carbon', color='red')

    plt.title('year vs land needed to sequester carbon content')

    plt.savefig('yvsc.png')

    if file_exists('static/yvsc.png'):
        os.replace('yvsc.png', 'static/yvsc.png')
    else:
        os.rename('yvsc.png', 'static/yvsc.png')

    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='forest_land', color='green')

    plt.title('year vs forest_land')

    plt.savefig('yvsfl.png')

    if file_exists('static/yvsfl.png'):
        os.replace('yvsfl.png', 'static/yvsfl.png')
    else:
        os.rename('yvsfl.png', 'static/yvsfl.png')

    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='fishing_ground',
                                                                                        color='green')

    plt.title('year vs fishing_ground')

    plt.savefig('yvsfg.png')

    if file_exists('static/yvsfg.png'):
        os.replace('yvsfg.png', 'static/yvsfg.png')
    else:
        os.rename('yvsfg.png', 'static/yvsfg.png')

    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='built_up_land',
                                                                                        color='green')

    plt.title('year vs built_up_land')

    plt.savefig('yvsbul.png')

    if file_exists('static/yvsbul.png'):
        os.replace('yvsbul.png', 'static/yvsbul.png')
    else:
        os.rename('yvsbul.png', 'static/yvsbul.png')

    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='crop_land',
                                                                                        color='green')

    plt.title('year vs crop_land')

    plt.savefig('yvscl.png')

    if file_exists('static/yvscl.png'):
        os.replace('yvscl.png', 'static/yvscl.png')
    else:
        os.rename('yvscl.png', 'static/yvscl.png')

    nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].plot(kind='scatter', x='year',
                                                                                        y='total',
                                                                                        color='green')

    plt.title('year vs total land')

    plt.savefig('yvst.png')

    if file_exists('static/yvst.png'):
        os.replace('yvst.png', 'static/yvst.png')
    else:
        os.rename('yvst.png', 'static/yvst.png')

    # calculate mean value of needed land for carbon sequester of country
    if ((country_select != 'None') & (record_select != 'None')) & ((country_select is not None) & (
            record_select is not None)):
        carbon_mean = nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].carbon.mean()
    else:
        carbon_mean = ''

    # calculate 2014 values of needed land for carbon sequester of country and total land available
    # Also analyze to declare if code red or code green and respective suggestion
    if ((country_select != 'None') & (record_select != 'None')) & ((country_select is not None) & (
            record_select is not None)):
        print(record_select)
        index = nfa.loc[
            (nfa['year'] == 2014) & (nfa['country'] == country_select) & (nfa['record'] == record_select)].index[0]
        carbon2014 = nfa.loc[
            (nfa['year'] == 2014) & (nfa['country'] == country_select) & (nfa['record'] == record_select), [
                'carbon']].iloc[[0], [0]]['carbon'][index]
        total2014 = nfa.loc[
            (nfa['year'] == 2014) & (nfa['country'] == country_select) & (nfa['record'] == record_select), [
                'total']].iloc[[0], [0]]['total'][index]
        row2014 = nfa.loc[
            (nfa['year'] == 2014) & (nfa['country'] == country_select) & (nfa['record'] == record_select), ['carbon',
                                                                                                            'total']]
        if row2014['carbon'][index] > row2014['total'][index]:
            code = '>> <b>Code Red</b>, implying that the situation is out of control in this country and the land distribution is not able to sequester the carbon. We suggest to decrease the carbon output or increase the land cover for sequestering the carbon content'
        else:
            code = '>> <b>Code Green</b>, implying that the situation is under control in this country and the land distribution is able in sequestering the carbon. We suggest measures be taken to maintain the composition'
    else:
        carbon2014 = ''
        total2014 = ''
        code = ''

    # clear the plot axes and draw pie chart
    plt.cla()

    if ((country_select != 'None') & (record_select != 'None')) & ((country_select is not None) & (
            record_select is not None)):
        pie2014 = nfa.loc[
            (nfa['year'] == 2014) & (nfa['country'] == country_select) & (nfa['record'] == record_select), ['crop_land',
                                                                                                            'grazing_land',
                                                                                                            'forest_land',
                                                                                                            'fishing_ground',
                                                                                                            'built_up_land']].values.flatten().tolist()
        plt.pie(pie2014, labels=['crop_land', 'grazing_land', 'forest_land', 'fishing_ground', 'built_up_land'])
    else:
        plt.pie([1], labels=[np.NaN])

    plt.title('land distribution pie chart for 2014')

    plt.savefig('pie2014.png')

    if file_exists('static/pie2014.png'):
        os.replace('pie2014.png', 'static/pie2014.png')
    else:
        os.rename('pie2014.png', 'static/pie2014.png')

    # convert the dataframe of description of selected rows in html format to render as table
    if ((country_select != 'None') & (record_select != 'None')) & ((country_select is not None) & (
            record_select is not None)):
        details = nfa.loc[(nfa['record'] == record_select) & (nfa['country'] == country_select)].describe().to_html()
    else:
        details = ''

    # render the template folder with html, etc and pass the variables with paths, strings and values
    return render_template('home.html', pie2014='static/pie2014.png', yvsbul='static/yvsbul.png',
                           yvscl='static/yvscl.png', yvst='static/yvst.png', yvsgl='static/yvsgl.png',
                           yvsc='static/yvsc.png', yvsfl='static/yvsfl.png', yvsfg='static/yvsfg.png', country=country,
                           record=record, country_select=country_select, record_select=record_select,
                           carbon_mean=carbon_mean, carbon2014=carbon2014, total2014=total2014, details=details,
                           code=code, stylesheet='static/css/stylesheet.css')


# to initiate the flask container
if __name__ == '__main__':
    app.run()
