import sys
import os
import json
import io
import uix
from uix.elements import row, col, input, button, textarea, form, div
from uix_components import basic_checkbox, basic_datalist
from uix import T

uix.html.add_css_file("_address_form.css",__file__)

class address_form(uix.Element):
    def __init__(self, id, callback=None):
        super().__init__(id=id)
        self.callback = callback
        self.setup_json_files()

        with div().cls("adress_form.css"):
            with form(id="myForm").cls("form-content").on("submit", self.add_address):
                with col().cls("address-grid"):
                    self.name = input(name="FirstName", placeholder=T("Name"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.surname = input(name="LastName", placeholder=T("Surname"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.phone = input(name="Phone", type="tel", placeholder=T("Phone"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    options = {T("Select Country"): T("Select Country"), **{country['code']: country['name'] for country in self.countries}}
                    self.country = basic_datalist(name="", id="countries", options=options, placeholder=T("Select Country"), required=True, callback=self.get_options)
                with col(id="hiddenAddress").cls("hidden address-grid") as hiddenAddress:
                    self.hiddenAddress = hiddenAddress
                    with row().style("height", "max-content"):
                        options_city = {key: key for key in self.address_data}
                        self.city = basic_datalist(name="", id="cities", options = options_city, placeholder=T("Select City"), callback=self.get_counties).style("width", "100%")                  
                        options_county = {"Select County": "Select County"}
                        self.counties = basic_datalist(name="", id="counties", options=options_county, placeholder=T("Select County"), callback=self.get_neighborhoods).style("width", "100%")                      
                    with row().style("height", "max-content"):
                        options_neighborhoods = {T("Select Neighborhood"): T("Select Neighborhood")}
                        self.neighborhoods = basic_datalist(name="",id="neighborhoods",options=options_neighborhoods, placeholder=T("Select Neighborhood") ,callback=self.set_neighborhoods)
                        self.neighborhoods.style("width","100%")
                with col().cls("address-grid"):
                    self.address = textarea(placeholder=T("Address"), required=True).style("height","90px").on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.addressTitle = input(placeholder=T("Address Title"), required=True).on("change", self.input_setter)
                with row().cls("address-grid"):
                    self.personalButton = button(T("Personal")).cls("personal-button").on("click", self.personal_click)
                    self.corporateButton = button(T("Corporate")).cls("cancel-button").on("click", self.corporate_click)
                with col(id="corporate").cls("hidden adress-grid") as corporate:
                    self.corporate = corporate           
                    with row().style("height", "max-content"):
                        self.vkn = input(placeholder=T("Tax Number")).on("change", self.input_setter)
                        self.companyName = input(placeholder=T("Company Name")).on("change", self.input_setter)
                    with row().style("height", "max-content"):
                        self.taxOffice = input(placeholder=T("Tax Office")).on("change", self.input_setter)
                        self.eFatura = basic_checkbox(id="efatura", label_text="E-Fatura Mükellefiyim").cls("eFatura-checkbox").style("display", "none")
                with row().cls("address-grid").style("height", "max-content"):
                    button("Add Billing Address", type="submit").cls("save-button")

    def setup_json_files(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        with io.open(os.path.join(current_path, 'address.json'),"r", encoding='utf-8') as address_json:
            data = address_json.read()
            address_json.close()
        self.address_data = json.loads(data)

        with io.open(os.path.join(current_path, 'ulke.json'),"r", encoding='utf-8') as country_json:
            country = country_json.read()
            country_json.close()
        self.countries = json.loads(country)

    def input_setter(self, ctx, id, value):
        ctx.elements[id].value = value

    def datalist_setter(self, input, value):
        input.value = value

    def personal_click(self, ctx, id, value):
        self.corporate.classes = ['col', 'hidden']
        self.corporateButton.set_style("background-color", "var(--background-secondary)")
        self.personalButton.set_style("background-color", "var(--ait)")
        self.vkn.attrs["required"] = False
        self.companyName.attrs["required"] = False
        self.taxOffice.attrs["required"] = False
        self.corporate.update()

    def corporate_click(self, ctx, id, value):
        self.corporate.classes = ['col', 'address-grid']
        self.corporate.remove_class("hidden")
        self.corporate.style("gap", "10px")
        self.personalButton.set_style("background-color", "var(--background-secondary)")
        self.corporateButton.set_style("background-color", "var(--ait)")
        self.vkn.attrs["required"] = True
        self.companyName.attrs["required"] = True
        self.taxOffice.attrs["required"] = True
        self.corporate.update()

    def get_options(self, ctx, id, value):
        if value != "Türkiye":
            self.hiddenAddress.classes = ['col', 'hidden']
            self.eFatura.style("display", "none")
            self.city.input.attrs["required"] = False
            self.counties.input.attrs["required"] = False
            self.neighborhoods.input.attrs["required"] = False
            self.hiddenAddress.update()
            self.corporate.update()
            self.datalist_setter(self.country, value)
        else:
            self.hiddenAddress.classes = ['col', 'address-grid']
            self.hiddenAddress.remove_class("hidden")
            self.eFatura.style("display", "flex")
            self.hiddenAddress.style("gap", "10px")
            self.city.input.attrs["required"] = True
            self.counties.input.attrs["required"] = True
            self.neighborhoods.input.attrs["required"] = True
            self.hiddenAddress.update()
            self.corporate.update()
            self.datalist_setter(self.country, value)

    def get_counties(self, ctx, id, value):
        self.city.value = value
        self.selected_city_counties = self.address_data.get(value, [])
        countiesData = {key: key for key in self.selected_city_counties}
        content = ctx.elements["counties"]
        self.datalist_setter(self.city,value)
        with content:
            self.counties = basic_datalist(name="", id="counties", placeholder=T("Select County"), required=True, options=countiesData, callback=self.get_neighborhoods)
        content.update()
        
    def get_neighborhoods(self, ctx, id, value):
        if self.selected_city_counties != None:
            self.selected_city_neighborhoods = self.selected_city_counties.get(value, [])
            neighborhoodsData = {key: key for key in self.selected_city_neighborhoods}
            content = ctx.elements["neighborhoods"]
            self.datalist_setter(self.counties,value)
            with content:
                self.neighborhoods = basic_datalist(name="", id="neighborhoods", placeholder=T("Select Neighborhood"), required=True, options=neighborhoodsData, callback=self.set_neighborhoods).style("width","100%")
            content.update()

    def set_neighborhoods(self, ctx, id, value):
        self.neighborhoods.value = value
        
    def add_address(self, ctx, id, value):
        address_form_data = {
            "name": self.name.value,
            "surname": self.surname.value,
            "phone": self.phone.value,
            "country": self.country.value,
            "city": self.city.value,
            "county": self.counties.value,
            "neighborhood": self.neighborhoods.value,
            "address": self.address.value,
            "addressTitle": self.addressTitle.value,
            "vkn": self.vkn.value,
            "companyName": self.companyName.value,
            "taxOffice": self.taxOffice.value,
            "eFatura": self.eFatura.checkbox.value
        }
        if self.callback:
            self.callback(self, ctx, id, address_form_data)

title = "Address Form"
description = """
# address_form(id)
1. Address Form Componenti
    | attribute     | desc                                                   |
    |---------------|--------------------------------------------------------|
    | id            | Komponentin id'si                                      |
    | callback      | Form submit edildiğinde çağırılacak fonksiyon          |
    """
sample = """
import uix
from uix_components import address_form
from uix_components._address_form._address_form import title, description, sample as code

def getformdata(self, id, ctx, data):
    print("Form Data:", data)
    
def address_form_example():
    root = address_form(id="deneme", callback=getformdata)
    return root
"""    