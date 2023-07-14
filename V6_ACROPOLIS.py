# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 10:25:52 2022

@author: nsilva
"""
import random
from pyproj import CRS
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Text
import os
import geopandas as gpd
import numpy as np
import pandas as pd
import joblib
from tkinter import messagebox
from PIL import ImageTk, Image
from tkintermapview import TkinterMapView
import sklearn
import sklearn.ensemble._forest
from pyproj import Proj
import csv
from pysheds.grid import Grid
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tkinter.filedialog import asksaveasfile
import math
import matplotlib.ticker as ticker
import rasterio
from rasterio.transform import xy
root=tk.Tk()
root.geometry('1300x700')
root.title('ACROPÓLIS: Clasificación de balsas frente al riesgo potencial con ML')

#Create main frame
main_frame=tk.Frame(root)
main_frame.pack(fill='both',expand=1)
#Create canvas
my_canvas=tk.Canvas(main_frame)
my_canvas.pack(side='left', fill='both', expand=1)
#Add scrollbar
my_scrollbar=ttk.Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
my_scrollbar.pack(side='right', fill='y')
#Configure canvas
scrollbarx=ttk.Scrollbar(main_frame, orient='horizontal', command=my_canvas.xview)
scrollbarx.pack(fill='x', side='bottom')
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
#Another frame inside canvas
second_frame=tk.Frame(my_canvas)
#Add the new frame
my_canvas.create_window((0,0), window=second_frame, anchor='nw')


    
my_menu=tk.Menu(root)
root.config(menu=my_menu)

'''def instrucciones():
    os.system('instrucciones.txt') '''

def mapa():
    X=x.get() #Balsa
    Y=y.get()
    cc=sco.get()
        
    if cc=='EPSG:25830 - ETRS89 / UTM zone 30N':
        myProj = Proj("+proj=utm +zone=30 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        lat,lon=myProj(X,Y, inverse=True)
        
        map_widget.set_position(lon, lat)
        map_widget.set_zoom(15)
        marker = map_widget.set_marker(lon,lat, text="Balsa")
    if cc=='EPSG:25831 - ETRS89 / UTM zone 31N':
        myProj = Proj("+proj=utm +zone=31 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        lat,lon=myProj(X,Y, inverse=True)
        map_widget.set_position(lon, lat)
        map_widget.set_zoom(15)
        marker = map_widget.set_marker(lon,lat, text="Balsa") 
        
    
def ascii_to_tiff(ascii_file_path, tiff_file_path):
    # Read the ASCII file content
    with open(ascii_file_path, 'r') as file:
        lines = file.readlines()

    # Parse header information
    header_info = {}
    for line in lines:
        if line.startswith("NCOLS"):
            header_info["NCOLS"] = int(line.split()[1])
        elif line.startswith("NROWS"):
            header_info["NROWS"] = int(line.split()[1])
        elif line.startswith("XLLCENTER"):
            header_info["XLLCENTER"] = float(line.split()[1])
        elif line.startswith("YLLCENTER"):
            header_info["YLLCENTER"] = float(line.split()[1])
        elif line.startswith("CELLSIZE"):
            header_info["CELLSIZE"] = float(line.split()[1])
        elif line.startswith("NODATA_VALUE"):
            header_info["NODATA_VALUE"] = float(line.split()[1])

    # Extract pixel values
    pixel_values = []
    for line in lines:
        if not any(line.startswith(header) for header in header_info.keys()):
            pixel_values.extend(line.split())

    # Convert valid pixel values to floats
    pixel_data = []
    for value in pixel_values:
        try:
            pixel_data.append(float(value))
        except ValueError:
            pass

    # Calculate the width and height of the image
    width = header_info["NCOLS"]
    height = header_info["NROWS"]

    # Create the grayscale image
    image = Image.new('F', (width, height))
    image.putdata(pixel_data)

   
    # Define the spatial reference information
    xllcenter = header_info["XLLCENTER"]
    yllcenter = header_info["YLLCENTER"]
    cellsize = header_info["CELLSIZE"]
    
    transform = rasterio.transform.from_origin(xllcenter, yllcenter +(cellsize * height), cellsize, cellsize)
    # Convert the image data to a NumPy array
    pixel_array = np.array(image)
    # Create the CRS object for EPSG:25830
    cc=sco.get()
    if cc=='EPSG:25830 - ETRS89 / UTM zone 30N':
        crs = CRS.from_epsg(25830)
    if cc=='EPSG:25831 - ETRS89 / UTM zone 31N':
        crs = CRS.from_epsg(25831)
    # Save the image as a TIFF file with the EPSG:25830 projection
    with rasterio.open(
        tiff_file_path,
        'w',
        driver='GTiff',
        width=width,
        height=height,
        count=1,
        dtype='float32',
        transform=transform,
        crs=crs
    ) as dst:
        dst.write(pixel_array, indexes=1)

def dem():
    
    
    f = filedialog.askopenfilename(filetypes=[("TIFF file", ".tif"), ("ASCII file", ".asc")], title="Open DEM file (.tif)") 
    # Check the file extension
    file_extension = os.path.splitext(f)[1]
   
    
    if file_extension == '.asc':
        # Convert ASCII to TIF
        tif_path = os.path.splitext(f)[0] + '.tif'
        ascii_to_tiff(f, tif_path)
        grid = Grid.from_raster(tif_path, data_name='dem')
        f=tif_path
        
    elif file_extension == '.tif':
        grid = Grid.from_raster(f, data_name='dem')
        
    class coorbalsa():
            X=x.get() #Balsa
            Y=y.get()
            balsa=[X,Y]
            
            
    elevDem=grid.dem[:-1,:-1]

    grid.fill_depressions(data='dem',out_name='flooded_dem')
    grid.resolve_flats(data='flooded_dem', out_name='inflated_dem')
    dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
    grid.flowdir(data='inflated_dem', dirmap=dirmap, out_name='dir')
    grid.accumulation(data='dir', dirmap=dirmap, out_name='acc', pad_inplace=False)
    accView=grid.view('acc', nodata=np.nan)
    plt.rc('xtick', labelsize=8)
    
   
    with rasterio.open(f) as src:
       # Read the elevation data as a numpy array
       elevation = src.read(1)
       shape = src.shape
       # Get the metadata for coordinate transformation
       transform = src.transform
       # Get the EPSG code of the source CRS
       source_crs = src.crs
    
    'Direction'
    # Get the coordinates of the origin point
    xx, yy = coorbalsa.balsa[0],coorbalsa.balsa[1]
    # Get the pixel coordinates of the origin
    X,Y = rasterio.transform.rowcol(transform, xx, yy)
    origin_pixel = rasterio.transform.rowcol(transform, xx, yy)
    origin_row, origin_col = origin_pixel[0],origin_pixel[1]
    
    'PATH'

   
    
    class main_path():
        # Select the path by checking neighboring pixels with higher values
        path = []
        current_row, current_col = origin_row, origin_col
        while True:
            path.append((current_row, current_col))
            neighbors = grid.acc[
                current_row - 1 : current_row + 2,
                current_col - 1 : current_col + 2
                ]
            max_idx = np.unravel_index(np.argmax(neighbors), neighbors.shape)
            max_row, max_col = current_row - 1 + max_idx[0], current_col - 1 + max_idx[1]
           
            if grid.acc[max_row, max_col] <= grid.acc[current_row, current_col]:
                break
            
            current_row, current_col = max_row, max_col
          
        path=pd.DataFrame(path, columns=['row','column'])
        path['x'], path['y'] = xy(transform, path['row'], path['column'])
        
    fig = plt.Figure(figsize = (18, 6),constrained_layout =False)
    cmap='terrain'
    plot1 = fig.add_subplot(121)
    im1=plot1.imshow(elevDem, extent=grid.extent, cmap=cmap)
    plot1.scatter(coorbalsa.balsa[0],coorbalsa.balsa[1], color='red', marker='v',s=150,label='Balsa')
    plot1.legend()
    
    
    plot1.set_title('Elevación del terreno', fontsize=16, fontweight="bold")
    divider=make_axes_locatable(plot1)
    cax = divider.append_axes('right', size='5%', pad=0.08)
    #fig.colorbar(im1, cax=cax, orientation='vertical', label='Elevación (m)')
        
    plot2 = fig.add_subplot(122)
    im2=plot2.imshow(accView, extent=grid.extent, cmap='cubehelix')
    plot2.scatter(main_path.path['x'], main_path.path['y'], marker='x', zorder=2, c='blue', s=4)
    plot2.scatter(coorbalsa.balsa[0],coorbalsa.balsa[1], color='red', marker='v',s=150,label='Balsa')
    plot2.legend()
    plot2.set_title('Acumulación', fontsize=16, fontweight="bold")
    
    divider = make_axes_locatable(plot2)
    cax = divider.append_axes('right', size='5%', pad=0.08)
    fig.colorbar(im2, cax=cax, orientation='vertical', label='Nª celdas aguas arriba')
        
       
    canvas = FigureCanvasTkAgg(fig, master = second_frame)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=13,columnspan=12)               
      

            
    def locaff():
                class loccoor():
                    param=[]
                    filepath = filedialog.askopenfilename(filetypes=[("CSV files", ".csv")], title="Open file") 
                    with open(filepath) as f:
                        reader = csv.DictReader(f, delimiter=';')
                        i=2
                        for row in reader:
                            i=i+1
                            idd=row['ID']
                            xc = row['x']
                            yc = row['y']    
                            tipo=row['tipo']
                            r=[idd,xc,yc,tipo]
                            param.append(r)
                        
                        param=pd.DataFrame(param,columns=['ID','x','y','tipo'])
                    
                redw= tk.Toplevel(root)
                redw.geometry("700x750")
                main_frame=tk.Frame(redw)
                main_frame.pack(fill='both',expand=1)
                 #Create canvas
                my_canvas=tk.Canvas(main_frame)
                my_canvas.pack(side='left', fill='both', expand=1)
                 #Add scrollbar
                my_scrollbar=ttk.Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
                my_scrollbar.pack(side='right', fill='y')
                 #Configure canvas
                my_canvas.configure(yscrollcommand=my_scrollbar.set)
                my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
                 #Another frame inside canvas
                frame=tk.Frame(my_canvas)
                 #Add the new frame
                my_canvas.create_window((0,0), window=frame, anchor='nw')
                
                xa=np.asarray(loccoor.param['x'])
                ya=np.asarray(loccoor.param['y'])
                xa=xa.astype(np.float)
                ya=ya.astype(np.float)
                
                class plot():
                
                    fig1, ax1=plt.subplots(figsize=(8,8))
                    ax1.scatter(xa,ya, label='Affecciones', s=70,marker='^', color='green')
                    ax1.scatter(main_path.path['x'], main_path.path['y'],s=5, label='Drenaje principal',color='brown')
                    ax1.legend(fontsize=12)
                    ax1.scatter(coorbalsa.balsa[0],coorbalsa.balsa[1], color='red', marker='v', label='Balsa', s=150)
                    ax1.legend()
                    ax1.grid()
                    ax1.set_title('Localización afecciones y red de drenaje', fontsize=16, fontweight="bold")
                    ax1.xaxis.set_major_locator(ticker.MultipleLocator(500))
                    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(100))
                    canvas = FigureCanvasTkAgg(fig1, master = frame)  
                    canvas.draw()
                    canvas.get_tk_widget().grid(row=8,columnspan=4, pady=10,padx=5) 
                    
                
                
                def ejes():
                    

                    xbalsa=coorbalsa.balsa[0]
                    ybalsa=coorbalsa.balsa[1]
                    rotacion=balsa.alpha.get()
                    
                    'Calcular ejes rotados'
                    alpha=rotacion*math.pi/180
                    y=np.arange(-1000,2000,20)
                    x=np.zeros(len(y))
                    
                    
                    ejebalsa=[]
                    for k in range(0,len(x)):
    
                        xp=(x[k]*math.cos(alpha)+y[k]*math.sin(alpha))+xbalsa
                        yp=(-1*x[k]*math.sin(alpha)+y[k]*math.cos(alpha))+ybalsa
                        r=[xp,yp]
                        ejebalsa.append(r)
   
                    ejebalsa=pd.DataFrame(ejebalsa, columns=['x','y'])
                    
                    x=np.arange(-500,4000,20)
                    y=np.zeros(len(x))
                    
                    ejebrecha=[]

                    for k in range(0,len(x)):
    
                        xp=(x[k]*math.cos(alpha)+y[k]*math.sin(alpha))+xbalsa
                        yp=(-1*x[k]*math.sin(alpha)+y[k]*math.cos(alpha))+ybalsa
                        r=[xp,yp]
                        ejebrecha.append(r)
   
                    ejebrecha=pd.DataFrame(ejebrecha, columns=['x','y'])
                    
                    
                    Xmin=main_path.path['x'].min()
                    Ymin=main_path.path['y'].min()
                    Xmax=main_path.path['x'].max()
                    Ymax=main_path.path['y'].max()
                    
                    
                    
                    lim=main_path.path.loc[main_path.path['x']>=Xmin]
                    lim1=lim.loc[lim['x']<=Xmax]
                    lim2=lim1.loc[lim1['y']<=Ymax]
                    
                    class mainc():
                        mainchannel=lim2.loc[lim2['y']>=Ymin]
                    
                    for item in plot.canvas.get_tk_widget().find_all():
                        plot.canvas.get_tk_widget().destroy()
                    
                    fig1, ax1=plt.subplots(figsize=(8,8))
                    ax1.scatter(xa,ya, label='Affecciones', s=70,marker='^',color='green')
                    #ax1.scatter(coorde.coord['x'],coorde.coord['y'],s=5, label='Red de drenaje',alpha=0.8, color='brown')
                    ax1.scatter(mainc.mainchannel['x'],mainc.mainchannel['y'],s=15, label='Vía Principal', color='blue')
                    ax1.scatter(xbalsa,ybalsa, s=150, marker='v', label='Balsa', color='red')
                    ax1.plot(ejebalsa['x'],ejebalsa['y'], label='Eje balsa', linestyle='--', color='black')
                    ax1.plot(ejebrecha['x'],ejebrecha['y'], label='Eje brecha', linestyle='--', color='green')
                    ax1.grid()
                    ax1.legend(fontsize=14)
                    ax1.set_title('Localización de los ejes, afecciones y drenaje principal', fontsize=16, fontweight="bold")
                    canvas = FigureCanvasTkAgg(fig1, master = frame)  
                    canvas.draw()
                    canvas.get_tk_widget().grid(row=8,columnspan=4, padx=10) 
                    
                    plot.canvas=canvas
                    
                    def distancias():
                        #new window
                        
                    #Al canal mainchannel
                        xaff=xa
                        yaff=ya
                        
                        xmain=np.asarray(mainc.mainchannel['x'])
                        ymain=np.asarray(mainc.mainchannel['y'])
                        dchannely=[]
                        
                        ang=balsa.alpha.get()
                        for k in range(0,len(xaff)):
                            dchannel=[]
                            for i in range(0,len(xmain)):
                                dis=math.sqrt(((xmain[i]-xaff[k])**2)+((ymain[i]-yaff[k])**2))
                                if ang>0 and ang <=180:
                                    if xaff[k]>=xmain[i]:
                                        s=1
                                    if xaff[k]<xmain[i]:
                                        s=-1 
                                if ang>180 and ang <=360:
                                    if xaff[k]>=xmain[i]:
                                        s=-1
                                    if xaff[k]<xmain[i]:
                                        s=1   
                                
                                r=[dis,s,k,i]
                                dchannel.append(r)        
                            dmin=min(dchannel)
                            f=[k+1,dmin[0]*dmin[1]]
                            dchannely.append(f)
                        dchannely=pd.DataFrame(dchannely, columns=['ID','D_channely'])
                        
                        #Al eje de la brecha
                        xb=np.asarray(ejebrecha['x'])
                        yb=np.asarray(ejebrecha['y'])
                        dresy=[]
                        for k in range(0,len(xaff)):
                            resy=[]
                            for i in range(0,len(xb)):
                                dis=math.sqrt((xb[i]-xaff[k])**2+(yb[i]-yaff[k])**2)   
                                
                                if ang>0 and ang <=180:
                                    if xaff[k]>=xb[i]:
                                        s=1
                                    if xaff[k]<xb[i]:
                                        s=-1 
                                if ang>180 and ang <=360:
                                    if xaff[k]>=xb[i]:
                                        s=-1
                                    if xaff[k]<xb[i]:
                                        s=1   
                                r=[dis,s,k,i,]
                                resy.append(r)    
                            dmin=min(resy)
                            f=[dmin[0]*dmin[1]]
                            dresy.append(f)
                        Dresy=pd.DataFrame(dresy, columns=['D_damy'])
                        #A la balsa
                        
                        xba=np.asarray(ejebalsa['x'])
                        yba=np.asarray(ejebalsa['y'])

                        
                        dresx=[]
                        for k in range(0,len(xaff)):
                            resx=[]
                            for i in range(0,len(xba)):
                                dis=math.sqrt((xba[i]-xaff[k])**2+(yba[i]-yaff[k])**2)    
                                r=[dis]
                                resx.append(r)    
                            dmin=min(resx)
                            f=[dmin[0]]
                            dresx.append(f)
                        Dresx=pd.DataFrame(dresx, columns=['D_damx'])
                        n=len(dchannely)
                        
                        #ML MODEL
                      
                        filename='2022feb_RF_RUS_BM.sav'
                        loaded_model = joblib.load(filename)
                        
    
                        Damloc=pd.DataFrame(np.full(n,[Bl.get()]),columns=['Damloc'])
                        slope_IA=pd.DataFrame(np.full(n,[Slb.get()]),columns=['slope_IA'])
                        trans_slope=pd.DataFrame(np.full(n,[St.get()]),columns=['trans_slope'])
                        long_slope=pd.DataFrame(np.full(n,[Slc.get()]),columns=['long_slope'])
                        initial_A=pd.DataFrame(np.full(n,[Lb.get()]),columns=['initial_A']) 
                        Wchannel=pd.DataFrame(np.full(n,[Wc.get()]),columns=['Wchannel_bottom'])
                        w_dam=pd.DataFrame(np.full(n,[Wr.get()]),columns=['w_dam'])        
                        l_dam=pd.DataFrame(np.full(n,[Lr.get()]),columns=['l_dam'])
                        h_dam=pd.DataFrame(np.full(n,[Hr.get()]),columns=['h_dam'])          
                        vol=pd.DataFrame(np.full(n,[voll.get()]),columns=['vol'])
                        hchannel=pd.DataFrame(np.full(n,[Hc.get()]),columns=['hchannel'])
                        manning=pd.DataFrame(np.full(n,[Manning.get()]),columns=['manning'])
        
                        malla=pd.concat([Damloc,slope_IA,trans_slope,long_slope,initial_A,Wchannel,w_dam,l_dam,h_dam,vol,
                                     hchannel,manning,Dresx['D_damx'],Dresy['D_damy'],
                                     dchannely['D_channely']], axis=1)
                    
                        
                        classprediction=loaded_model.predict(malla)
                        f=[]
                        for k in range(0,len(classprediction)):
                            a=classprediction[k]
                            if a==1:
                                riesgo='Grave'
                                f.append(riesgo)
                            if a==0:
                                riesgo='No Grave'
                                f.append(riesgo)
                        f=pd.DataFrame(f, columns=['Riesgo']) 
                        
                        results=f
                     
                        r1=results.loc[results['Riesgo']=='Grave']
                        tip=loccoor.param['tipo']
                        final=pd.concat([results,tip],axis=1)
                      
                        
                        vivienda=final.loc[final['tipo']=='vivienda']
                        material=final.loc[final['tipo']=='daños materiales']
                        esen=final.loc[final['tipo']=='servicio esencial']
                        ambna=final.loc[final['tipo']=='protección nacional']
                        ambau=final.loc[final['tipo']=='protección autonómica']
                        via=final.loc[final['tipo']=='vía local']
                        vin=final.loc[final['tipo']=='vía principal']
                        
                        grvivi=vivienda.loc[vivienda['Riesgo']=='Grave']
                        grmat=material.loc[material['Riesgo']=='Grave']
                        gresen=esen.loc[esen['Riesgo']=='Grave']
                        grambna=ambna.loc[ambna['Riesgo']=='Grave']
                        grambau=ambau.loc[ambau['Riesgo']=='Grave']
                        viloc=via.loc[via['Riesgo']=='Grave']
                        vinoc=vin.loc[vin['Riesgo']=='Grave']
                        
                        if len(grvivi)>=5 or len(grmat)>=50 or len(gresen)>=1 or len(grambna)>=1 or len(vinoc)>=1:
                            cate='A'
                        if (len(grvivi)>=1 and len(grvivi)<5) or (len(grmat)>=10 and len(grmat)<50) or (len(grambau)>=1 and len(grambna)==0) or (len(viloc)>0):
                            cate='B'
                        if len(grvivi)==0 and len(grmat)<10 and len(gresen)==0 and len(grambna)==0 and len(grambau)==0 and len(viloc)==0 and len(vinoc)==0:
                            cate='C'
                        
                        
            
                        idd=np.arange(0,len(xa),1)
                        risk=np.asarray(results['Riesgo'])
                        RISK=pd.DataFrame(risk, columns=['Riesgo'])
                        I=pd.DataFrame(idd, columns=['id'])
                        data=pd.concat([I,loccoor.param['x'],loccoor.param['y'],RISK], axis=1)
                        data["x"] = pd.to_numeric(data["x"], downcast="float")
                        data["y"] = pd.to_numeric(data["y"], downcast="float")
                        grave=data.loc[data['Riesgo']=='Grave']
                        nograve=data.loc[data['Riesgo']=='No Grave']
                       
                        
                        fig1, ax1=plt.subplots(figsize=(8,8))
                       
                        ax1.scatter(mainc.mainchannel['x'],mainc.mainchannel['y'],s=15, label='Drenaje principal', alpha=0.2,color='brown')
                        ax1.scatter(nograve['x'],nograve['y'], marker='^', color='blue', s=150, label='Riesgo No Grave')    
                        ax1.scatter(grave['x'],grave['y'], marker='^', color='red', s=120, label='Riesgo Grave')
                        
                        ax1.scatter(xbalsa,ybalsa, s=150, marker='v', label='Balsa', color='black')
                        ax1.plot(ejebalsa['x'],ejebalsa['y'], label='Eje balsa', linestyle='--', color='black')
                        ax1.plot(ejebrecha['x'],ejebrecha['y'], label='Eje brecha', linestyle='--', color='green')
                        ax1.grid()
                        ax1.legend(fontsize=14)
                        '''for i in range(len(idd)):
                            ax1.annotate(idd[i], (x[i], y[i] + 0.2))'''
                        canvas = FigureCanvasTkAgg(fig1, master = frame)  
                        canvas.draw()
                        canvas.get_tk_widget().grid(row=8,columnspan=4, pady=10) 
                        plot.canvas=canvas
                      
                        
                        cat_label=tk.Label(frame, text = 'Categoría Balsa', font = ('calibre',10,'bold'))
                        cat_label.grid(row=11, column=1, pady=10)
                        cat_entry=tk.Entry(frame, font = ('calibre',10,'bold'))
                        cat_entry.insert(0,cate)
                        cat_entry.grid(row=11, column=2, pady=10)
                        tk.Label(frame, text='ID', font = ('calibre',12,'bold')).grid(row=12,column=1)
                        tk.Label(frame, text='Clasificación de riesgo', font = ('calibre',12,'bold')).grid(row=12,column=2)
                        tk.Label(frame, text='Tipo de afección', font = ('calibre',12,'bold')).grid(row=12,column=3)
                        
                        def esto():
                         
                            def nextt(): 
                          
                        
                                tk.Label(frame, text='Iteraciones (%)', font = ('calibre',12,'bold')).grid(row=12,column=4)
                                p=0.05
                                dx=np.asarray(Dresx['D_damx'])
                                dy=np.asarray(Dresy['D_damy'])
                                dc=np.asarray(dchannely['D_channely'])
                                nr= []
                                pred=pd.DataFrame()
                                loop=nu.get()
                                for ll in range (0,loop):
                                    Bln=random.uniform((Bl.get()-(Bl.get()*p)), (Bl.get()+(Bl.get()*p)))
                                    Slbn=random.uniform((Slb.get()-(Slb.get()*p)), (Slb.get()+(Slb.get()*p)))
                                    Stn=random.uniform((St.get()-(St.get()*p)), (St.get()+(St.get()*p)))
                                    Slcn=random.uniform((Slc.get()-(Slc.get()*p)), (Slc.get()+(Slc.get()*p)))
                                    Lbn=random.uniform((Lb.get()-(Lb.get()*p)),(Lb.get()+(Lb.get()*p)))
                                    Wcn=random.uniform((Wc.get()-(Wc.get()*p)), (Wc.get()+(Wc.get()*p)))
                                    Wrn=random.uniform((Wr.get()-(Wr.get()*p)), (Wr.get()+(Wr.get()*p)))
                                    Lrn=random.uniform((Lr.get()-(Lr.get()*p)), (Lr.get()+(Lr.get()*p)))
                                    Hrn=random.uniform((Hr.get()-(Hr.get()*p)), (Hr.get()+(Hr.get()*p)))
                                    voln=random.uniform((voll.get()-(voll.get()*p)), (voll.get()+(voll.get()*p)))
                                    Hcn=random.uniform((Hc.get()-(Hc.get()*p)), (Hc.get()+(Hc.get()*p)))
                                    mann=random.uniform((Manning.get()-(Manning.get()*p)), (Manning.get()+(Manning.get()*p)))
                                    for kk in range (0,n):
                                        DX=random.uniform((dx[kk]-dx[kk]*p),(dx[kk]+dx[kk]*p))
                                        DY=random.uniform((dy[kk]-dy[kk]*p),(dy[kk]+dy[kk]*p))
                                        DC=random.uniform((dc[kk]-dc[kk]*p),(dc[kk]+dc[kk]*p))
                                        r=[DX,DY,DC]
                                        nr.append(r)
                                    dis=pd.DataFrame(nr,columns=['D_damx','D_damy','D_channely'])
                                    nr=[]
                            
                                    new_malla=pd.concat([pd.DataFrame(np.full(n,Bln),columns=['Damloc']),
                                                 pd.DataFrame(np.full(n,Slbn),columns=['slope_IA']),
                                                 pd.DataFrame(np.full(n,Stn),columns=['trans_slope']),
                                                 pd.DataFrame(np.full(n,Slcn),columns=['long_slope']),
                                                 pd.DataFrame(np.full(n,Lbn),columns=['initial_A']),
                                                 pd.DataFrame(np.full(n,Wcn),columns=['Wchannel_bottom']),
                                                 pd.DataFrame(np.full(n,Wrn),columns=['w_dam']),
                                                 pd.DataFrame(np.full(n,Lrn),columns=['l_dam']),
                                                 pd.DataFrame(np.full(n,Hrn),columns=['h_dam']),
                                                 pd.DataFrame(np.full(n,voln),columns=['vol']),
                                                 pd.DataFrame(np.full(n,Hcn),columns=['hchannel']),
                                                 pd.DataFrame(np.full(n,mann),columns=['manning']),
                                                 dis
                                                 ], axis=1)
                            
                                    classprediction=loaded_model.predict(new_malla)
                                    pred=pd.concat([pred, pd.DataFrame(classprediction)], axis=1)
                            
                                #Count classification
                                pred['sum']=pred.sum(axis=1)
                                pred['%']=(pred['sum']/loop*100)
                                  
                                per=np.asarray(pred['%'])
                                for k in range(0, len(classprediction)):                        
                                    r=risk[k]                            
                                    perc=per[k]                          
                                    if r=='Grave':                              
                                        tk.Label(frame, text=round(perc,2), font = ('calibre',12),fg='black').grid(row=k+13,column=4)
                                    if r=='No Grave':
                                        tk.Label(frame, text=round((100-perc),2), font = ('calibre',12),fg='black').grid(row=k+13,column=4)
                            
                            redw= tk.Toplevel(root)
                            redw.geometry("300x100")
                            main_frame=tk.Frame(redw)
                            main_frame.pack(fill='both',expand=1)
                            nu=tk.IntVar()
                            tk.Label(main_frame, text='Nª iteraciones', font = ('calibre',10,'bold'),padx=5, pady=5).grid(row=2,column=1)
                            tk.Entry(main_frame, textvariable = nu, font = ('calibre',10,'normal')).grid(row=2,column=2)
                            tk.Button(main_frame, text ='Aceptar', command=nextt, font = ('calibre',10,'bold'),padx=5, pady=5).grid(row=3,columnspan=2)
                        tk.Button(frame, text ='Análisis estocástico', command=esto, font = ('calibre',10,'bold'),padx=5, pady=5).grid(row=11,column=3)
                        
                        t=np.asarray(tip)
                        for k in range(0, len(classprediction)):
                                iD=idd[k]+1
                                r=risk[k]
                                tipp=t[k] 
                          
                                if r=='Grave':    
                                    tk.Label(frame, text=iD, font = ('calibre',12),fg='red').grid(row=k+13,column=1)
                                    tk.Label(frame, text=r, font = ('calibre',12),fg='red').grid(row=k+13,column=2)
                                    tk.Label(frame, text=tipp, font = ('calibre',12),fg='black').grid(row=k+13,column=3)                               
                                if r=='No Grave':
                                    tk.Label(frame, text=iD, font = ('calibre',12)).grid(row=k+13,column=1)
                                    tk.Label(frame, text=r, font = ('calibre',12)).grid(row=k+13,column=2)
                                    tk.Label(frame, text=tipp, font = ('calibre',12),fg='black').grid(row=k+13,column=3) 
                            
                        
                    
                    dis_btn=tk.Button(frame,text ='Calcular riesgo', command=distancias, font = ('calibre',10,'bold'))
                    dis_btn.grid(row=10, columnspan=4, padx=5, pady=10)
                    
   
                class balsa():
                    x=tk.DoubleVar()
                    y=tk.DoubleVar()
                    alpha=tk.DoubleVar()
                    
                eje_label=tk.Label(frame, text='Calcular ejes de la brecha y balsa',font = ('calibre',10,'bold'))
                eje_label.grid(row=0, columnspan=4, padx=5,pady=2)
                
                alpha_label=tk.Label(frame, text = 'Ángulo', font = ('calibre',10,'bold'))
                alpha_entry=tk.Entry(frame,textvariable=balsa.alpha,font = ('calibre',10,'normal'))
                alpha_label.grid(row=1, column=0, padx=5)
                alpha_entry.grid(row=1,column=1, padx=5)
                
              
            
                      
        
                
                acept_btn=tk.Button(frame,text ='Aceptar', command=ejes, font = ('calibre',10,'bold'))
                acept_btn.grid(row=5, column=1, padx=5)
                
                def visor():
                    redw= tk.Toplevel(root)
                    redw.geometry("500x500")
                    main_frame=tk.Frame(redw)
                    main_frame.pack(fill='both',expand=1)
                    #Create canvas
                    my_canvas=tk.Canvas(main_frame)
                    my_canvas.pack(side='left', fill='both', expand=1)
                    #Add scrollbar
                    my_scrollbar=ttk.Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
                    my_scrollbar.pack(side='right', fill='y')
                    #Configure canvas
                    my_canvas.configure(yscrollcommand=my_scrollbar.set)
                    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
                    #Another frame inside canvas
                    visorframe=tk.Frame(my_canvas)
                    #Add the new frame
                    my_canvas.create_window((0,0), window=visorframe, anchor='nw')
                    
                    if projection.cc=='EPSG:25830 - ETRS89 / UTM zone 30N':
                        myProj = Proj("+proj=utm +zone=30 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
                  
                    if projection.cc=='EPSG:25831 - ETRS89 / UTM zone 31N':
                        myProj = Proj("+proj=utm +zone=31 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
                    lat,lon=myProj(coorbalsa.balsa[0],coorbalsa.balsa[1], inverse=True)
                    map_widget = TkinterMapView(visorframe, width=500, height=500, corner_radius=0)
                    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
                    map_widget.pack()
                    map_widget.set_position(lon, lat)  
                    map_widget.set_zoom(15)
                    marker = map_widget.set_marker(lon,lat, text="Balsa")
                    #markers AoI
                    for i in range(0,len(xa)):
                            lat,lon=myProj(xa[i],ya[i], inverse=True)
                            marker2 = map_widget.set_marker(lon,lat, text="ID {}".format(i+1))
                
                visor.btn=tk.Button(frame,text ='Ver afecciones', command=visor, font = ('calibre',10,'bold'))
                visor.btn.grid(row=5, column=3, padx=5)
                
                
            
    affecciones_btn=tk.Button(second_frame,text ='Seleccionar AoI', command=locaff, font = ('calibre',10,'bold'))
    affecciones_btn.grid(row=17, columnspan=12, padx=5)
    
    
    
    
def cont():
    title_label=tk.Label(second_frame, text = 'Red de drenaje', font = ('calibre',12,'bold'),padx=10, pady=10)
    title_label.grid(row=11,columnspan=17)
    ttk.Label(second_frame, text = "Abrir archivo MED", 
        font = ('calibre',10,'bold')).grid(row=12,column=4, pady=8)
    tk.Button(second_frame,text ='Abrir', command=dem, font = ('calibre',10,'bold')).grid(row=12,column=5, pady=8)
    

def geo():
    redw= tk.Toplevel(root)
    redw.geometry("1000x600")
    main_frame=tk.Frame(redw)
    main_frame.pack(fill='both',expand=1)
    myimg2=Image.open('Planview.png')
    r_img2=myimg2.resize((550,300))
    img2=ImageTk.PhotoImage(r_img2)
    panel =tk.Label(main_frame, image = img2)
    panel.image = img2
    
    myimg3=Image.open('vistalat.png')
    r_img3=myimg3.resize((450,300))
    img3=ImageTk.PhotoImage(r_img3)
    panel2 =tk.Label(main_frame, image = img3)
    panel2.image = img3
    
    panel.grid(row=1, column=0)
    panel2.grid(row=1, column=1)
    tk.Label(main_frame, text = 'Geometría sintética', font = ('calibre',12,'bold'),padx=5, pady=5).grid(row=0, columnspan=3)
    tk.Label( main_frame, text='Wr: Ancho de la balsa (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=2, column=0)
    tk.Label( main_frame, text='Lr: Largo de la balsa (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=2, column=1)
    tk.Label( main_frame, text='Bl: Distancia balsa al canal (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=3, column=0)
    tk.Label( main_frame, text='Slb: Pendiente longitudinal sección B (%)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=3, column=1)
    tk.Label( main_frame, text='Slc: Pendiente longitudinal sección C (%)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=4, column=0)
    tk.Label( main_frame, text='St: Pendiente transversal sección C (%)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=4, column=1)
    tk.Label( main_frame, text='LB: Longitud sección B (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=5, column=0)
    tk.Label( main_frame, text='Wc: Ancho canal (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=5, column=1)
    tk.Label( main_frame, text='Hc: Profundidad canal (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=6, column=0)
    tk.Label( main_frame, text='Hr: Profundidad balsa (m)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=6, column=1)
    tk.Label( main_frame, text='Volume:Volumen balsa (hm3)',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=7, column=0)
    tk.Label( main_frame, text='Manning: Rugosidad terreno',font = ('calibre',11,'normal'),padx=5, pady=5).grid(row=7, column=1)
    
    
    
    
file_menu=tk.Menu(my_menu)
my_menu.add_cascade(label='Proyecto',font = ('calibre',11,'bold'), menu=file_menu)
file_menu.add_command(label='Geometría', command=geo)






'''imgPI=Image.open('pi.png')
r_imgPI=imgPI.resize((550,350))
imgPI=ImageTk.PhotoImage(r_imgPI)'''

# declaring variable
# for storing 
Bl=tk.DoubleVar()
Wr=tk.DoubleVar()
Lr=tk.DoubleVar()
Hr=tk.DoubleVar()
Wc=tk.DoubleVar()
St=tk.DoubleVar()
Slc=tk.DoubleVar()
Slb=tk.DoubleVar()
Hc=tk.DoubleVar()
Lb=tk.DoubleVar()
Manning=tk.DoubleVar()
voll=tk.DoubleVar()
x=tk.DoubleVar()
y=tk.DoubleVar()


# name using widget Entry and labels
Bl_label=tk.Label(second_frame, text = 'Bl (m)', font = ('calibre',10,'bold'))
Bl_entry = tk.Entry(second_frame,textvariable = Bl, font=('calibre',10,'normal'))  
Wr_label = tk.Label(second_frame, text = 'Wr (m)', font = ('calibre',10,'bold'))
Wr_entry=tk.Entry(second_frame, textvariable = Wr, font = ('calibre',10,'normal'))
Lr_label = tk.Label(second_frame, text = 'Lr (m)', font = ('calibre',10,'bold'))
Lr_entry=tk.Entry(second_frame, textvariable = Lr, font = ('calibre',10,'normal'))
Hr_label = tk.Label(second_frame, text = 'Hr (m)', font = ('calibre',10,'bold'))
Hr_entry=tk.Entry(second_frame, textvariable = Hr, font = ('calibre',10,'normal'))
Wc_label = tk.Label(second_frame, text = 'Wc (m)', font = ('calibre',10,'bold'))
Wc_entry=tk.Entry(second_frame, textvariable = Wc, font = ('calibre',10,'normal'))
St_label = tk.Label(second_frame, text = 'St (%)', font = ('calibre',10,'bold'))
St_entry=tk.Entry(second_frame, textvariable = St, font = ('calibre',10,'normal'))
Slc_label = tk.Label(second_frame, text = 'Slc (%)', font = ('calibre',10,'bold'))
Slc_entry=tk.Entry(second_frame, textvariable = Slc, font = ('calibre',10,'normal'))
Slb_label = tk.Label(second_frame, text = 'Slb (%)', font = ('calibre',10,'bold'))
Slb_entry=tk.Entry(second_frame, textvariable = Slb, font = ('calibre',10,'normal'))
Hc_label = tk.Label(second_frame, text = 'Hc (m)', font = ('calibre',10,'bold'))
Hc_entry=tk.Entry(second_frame, textvariable = Hc, font = ('calibre',10,'normal'))
Lb_label = tk.Label(second_frame, text = 'Lb (m)', font = ('calibre',10,'bold'))
Lb_entry=tk.Entry(second_frame, textvariable = Lb, font = ('calibre',10,'normal'))
manning_label = tk.Label(second_frame, text = 'Manning (m/s1/3)', font = ('calibre',10,'bold'))
manning_entry=tk.Entry(second_frame, textvariable = Manning, font = ('calibre',10,'normal'))
vol_label = tk.Label(second_frame, text = 'Volume (Hm3)', font = ('calibre',10,'bold'))
vol_entry=tk.Entry(second_frame, textvariable = voll, font = ('calibre',10,'normal'))



ttk.Label(second_frame, text = "Sistema de coordenadas :", 
        font = ('calibre',10,'bold')).grid(row=2,column=3, pady=10)
n = tk.StringVar()
sco = ttk.Combobox(second_frame, width = 35, 
                            textvariable = n)
sco['values'] = ('EPSG:25830 - ETRS89 / UTM zone 30N', 
                          'EPSG:25831 - ETRS89 / UTM zone 31N',)
sco.grid(column = 5, row = 2)
sco.current(0) 



x_label=tk.Label(second_frame, text = 'UTMx', font = ('calibre',10,'bold'))
x_entry=tk.Entry(second_frame, textvariable = x, font = ('calibre',10,'normal'))
y_label=tk.Label(second_frame, text = 'UTMy', font = ('calibre',10,'bold'))
y_entry=tk.Entry(second_frame, textvariable = y, font = ('calibre',10,'normal'))
x_label.grid(row=3,column=2)
x_entry.grid(row=3,column=3)
y_label.grid(row=3,column=5)
y_entry.grid(row=3,column=6)

map_btn=tk.Button(second_frame, text='Buscar', command=mapa, font = ('calibre',10,'bold'))
map_btn.grid(row=4, columnspan=12)
# create map widget
map_widget = TkinterMapView(second_frame, width=1400, height=400, corner_radius=0)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
map_widget.grid(row=5, columnspan=12, padx=20, pady=10)
map_widget.set_position(38, -0.8)  
map_widget.set_zoom(8)

   
title_label=tk.Label(second_frame, text = 'Paramétros físicos', font = ('calibre',12,'bold'),padx=10, pady=10)
title_label.grid(row=6,columnspan=12)
Bl_label.grid(row=7,column=0)
Bl_entry.grid(row=7,column=1)
Wr_label.grid(row=7,column=2)
Wr_entry.grid(row=7,column=3)
Lr_label.grid(row=7,column=4)
Lr_entry.grid(row=7,column=5)
Hr_label.grid(row=7,column=6)
Hr_entry.grid(row=7,column=7)
Wc_label.grid(row=8,column=0)
Wc_entry.grid(row=8,column=1)
St_label.grid(row=8,column=2)
St_entry.grid(row=8,column=3)
Slc_label.grid(row=8,column=4)  
Slc_entry.grid(row=8,column=5)
Slb_label.grid(row=8,column=6)
Slb_entry.grid(row=8,column=7)
Hc_label.grid(row=9,column=0)
Hc_entry.grid(row=9,column=1)
Lb_label.grid(row=9,column=2)
Lb_entry.grid(row=9,column=3)
manning_label.grid(row=9,column=4)
manning_entry.grid(row=9,column=5)
vol_label.grid(row=9,column=6)
vol_entry.grid(row=9,column=7)

cont_bt=tk.Button(second_frame,text ='Continuar', command=cont, font = ('calibre',10,'bold'))
cont_bt.grid(row=10, columnspan=12,padx=10, pady=20)



root.mainloop()