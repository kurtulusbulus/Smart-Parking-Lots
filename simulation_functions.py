#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#function for creating new agent based on mu and sigma 
def create_agent(mu,sigma,mu_stay,sigma_stay):
    cars_arrive=[]
    cars_stay=[]
    arrive_time = abs(round(np.random.normal(mu, sigma, 1)[0]))
    cars_arrive.append(arrive_time)
    stay_time = abs(round(np.random.normal(mu_stay, sigma_stay,1)[0]))
    cars_stay.append(stay_time)    
    return cars_arrive,cars_stay




def create_population(num_of_agents,num_of_days):
    
    morning=[i for i in range(6*60,12*60)]
    afternoon=[i for i in range(12*60,18*60)]
    night=[i for i in range(18*60,23*60)]
    day_stay=[i for i in range(20,5*60)]
    night_stay=[i for i in range(6*60,9*60)]
    mu_morning=np.mean(morning)
    mu_afternoon=np.mean(afternoon)
    mu_night=np.mean(night)
    mu_day=np.mean(day_stay)
    mu_night=np.mean(night_stay)
    sigma_stay=30
    sigma_arrive =2.8*60

    num_of_cars=num_of_agents
    time=num_of_days
    cars=[]

    for i in range(num_of_cars):
        flag_integers=[1,2,3]
        day_integers=[i for i in range(time)]
        mu_flag=np.mean(flag_integers)
        sigma_flag=mu_flag/10
        s_flag=abs(round(np.random.normal(mu_flag,sigma_flag,1)[0]))
        flag=s_flag
    
        if flag==1: #morning
            mu_day_integers=np.mean(day_integers)
            s_day=abs(round(np.random.normal(mu_day_integers,1,1)[0])) #choosing the day randomly
            new_mu=s_day*1440+mu_morning
            cars.append(create_agent(new_mu,sigma_arrive,mu_day,sigma_stay))                     
        
        elif flag==2: #afternoon
            mu_day_integers=np.mean(day_integers)
            s_day=abs(round(np.random.normal(mu_day_integers,1,1)[0])) #choosing the day randomly
            new_mu=s_day*1440+mu_afternoon
            cars.append(create_agent(new_mu,sigma_arrive,mu_day,sigma_stay)) 
                   
        elif flag==3: #night
            mu_day_integers=np.mean(day_integers)
            s_day=abs(round(np.random.normal(mu_day_integers,1,1)[0])) #choosing the day randomly
            new_mu=s_day*1440+mu_night
            cars.append(create_agent(new_mu,sigma_arrive,mu_night,sigma_stay)) 
    
    
    cars=np.squeeze(np.asarray(cars))    
    cars_check_out=cars[:,0]+cars[:,1]
    cars=np.concatenate((cars,cars_check_out.reshape(-1,1)),axis=1)

    
    return cars


def find_arriving_car(min_car,list_car):
    arrived_car=[]
    for i in range(len(list_car)):
        if min_car==list_car[i]:
            arrived_car.append(i)
            
    return arrived_car 


def find_leaving_car(min_car,list_car):
    leaving_car=[]
    for i in range(len(list_car)):
        if min_car==list_car[i]:
            leaving_car.append(i)
            
    return leaving_car 


def parking_the_car(car_ID,parking_lots):
    for i in range(len(parking_lots)):
        if parking_lots[i]==-1:
            parking_lots[i]=car_ID
            break
        
    return parking_lots


def removing_the_car(car_ID,parking_lots):
    for i in range(len(parking_lots)):
        if parking_lots[i]==car_ID:
            parking_lots[i]=-1
            break
    return parking_lots



def start_simulation(num_of_days,total_car,lot_number):
    log_matrix=['Min','Car ID','State']
    parking_lot_matrix=np.ones(lot_number+1)*-1
    parking_lot_matrix=np.reshape(parking_lot_matrix,(1,-1))
    minute=0
    num_arrived=0
    num_leaving=0
    num_arrived_list=[]
    num_leaved_list=[]

    parking_temp=np.ones(lot_number)*-1   
    cars=create_population(total_car,num_of_days)
    check_in=cars[:,0]
    check_out=cars[:,2]
    num_of_cars_in_park=[]
    
    while minute<num_of_days*1440: 
        
        arrivers=[]
        leavers=[]
        for i in range(cars.shape[0]):
            if minute==check_in[i]:
                arrivers.append(i)
            if minute==check_out[i]:
                leavers.append(i)
                
        num_arrived_list.append(len(arrivers))
        num_leaved_list.append(len(leavers))
                    
        for i in range(len(arrivers)):
            parking_temp=parking_the_car(arrivers[i],parking_temp)
        time_park=np.array([minute])
        new_parking_lots=np.concatenate((time_park,parking_temp),axis=0)
        #print(parking_lot_matrix.shape)
        #print(new_parking_lots.shape)
        
        new_parking_lots=np.reshape(new_parking_lots,(1,-1))
        #print(parking_lot_matrix.shape)    
        #print(new_parking_lots.shape)
        parking_lot_matrix=np.concatenate((parking_lot_matrix,new_parking_lots),axis=0)
        #print(parking_lot_matrix.shape)    
        #print(new_parking_lots.shape)
        for i in range(len(leavers)):
            parking_temp=removing_the_car(leavers[i],parking_temp)
        
        num_arrived=num_arrived+len(arrivers)
        num_leaving=num_leaving+len(leavers)
        num_of_cars_in_park.append(num_arrived-num_leaving)
        for j in range(len(arrivers)):
            log_matrix=np.vstack([log_matrix,[minute,arrivers[j],'IN']])
        for j in range(len(leavers)):
            log_matrix=np.vstack([log_matrix,[minute,leavers[j],'OUT']])   
         
        print((minute/(num_of_days*1440))*100,end="\r")
        minute=minute+1
    return parking_lot_matrix,log_matrix,num_of_cars_in_park,num_arrived_list,num_leaved_list

