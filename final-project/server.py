#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# if __name__ == '__main__':

from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from controllers import controller

app = FastAPI()
app.mount("/static", StaticFiles(directory="views/public"))

@app.get("/")
def shalom():
    return controller.getIndexPage()

@app.post("/landgen")
def example(data = Body()):
    return controller.generateLand(data)

@app.post("/landgen/zip")
def hello(data = Body()):
    return controller.createZip(data)