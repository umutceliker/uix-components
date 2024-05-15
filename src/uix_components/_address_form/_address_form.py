import os
import json
import io
import uix
from uix.elements import row, col, input, button, div
from uix_components import basic_checkbox, basic_datalist
from uix import T

uix.html.add_css_file("_address_form.css",__file__)

class address_form(uix.Element):
    def __init__(self, id, callback=None):
        super().__init__(id=id)
        self.callback = callback
        self.setup_json_files()
        self.city_value = None
        self.counties_value = None
        self.isCorporate = False
        with div():
            with div(id="myForm").cls("default-address"):
                with col().cls("address-grid"):
                    self.name = input(name="FirstName", placeholder=T("Name"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.surname = input(name="LastName", placeholder=T("Surname"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.zip_code = input(name="ZipCode", type="tel", placeholder=T("Zip Code"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    options = {T("Select Country"): T("Select Country"), **{country['code']: country['name'] for country in self.countries}}
                    self.country = basic_datalist(name="", id="countries", options=options, placeholder=T("Select Country"), required=True, callback=self.get_options)
                with col(id="turkey_addressFormat").cls("hidden address-grid").style("gap","10px") as turkey_addressFormat:
                    self.turkey_addressFormat = turkey_addressFormat
                    with row().style("height", "max-content"):
                        options_city = {key: key for key in self.address_data}
                        self.city_datalist = basic_datalist(name="", id="cities", options = options_city, placeholder=T("Select City"), callback=self.get_counties).style("width", "100%")                  
                        options_county = {"Select County": "Select County"}
                        self.counties_datalist = basic_datalist(name="", id="counties", options=options_county, placeholder=T("Select County"), callback=self.get_neighborhoods).style("width", "100%")                      
                    with row().style("height", "max-content"):
                        options_neighborhoods = {T("Select Neighborhood"): T("Select Neighborhood")}
                        self.neighborhoods = basic_datalist(name="",id="neighborhoods",options=options_neighborhoods, placeholder=T("Select Neighborhood") ,callback=self.set_neighborhoods)
                        self.neighborhoods.style("width","100%")
                with col(id="default_addressFormat").cls("address-grid") as default_addressFormat:
                    self.default_addressFormat = default_addressFormat
                    with row().style("height", "max-content"):
                        self.city = input(placeholder=T("City"), required=True).on("change", self.input_setter)
                        self.region = input(placeholder=T("Region"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.address_line1 = input(placeholder=T("Address Line 1 (house number, street name, and suffix)"), required=True).on("change", self.input_setter)
                with col().cls("address-grid"):
                    self.address_line2 = input(placeholder=T("Address Line 2 (apartment, suite, unit number, room)"), required=True).on("change", self.input_setter)
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
                    self.add_button=button(id=self.id+"-button",value=T("Add Billing Address")).cls("save-button").on("click", self.add_address)

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
        ctx.elements[id].value = value.upper()

    def datalist_setter(self, input, value):
        input.value = value

    def personal_click(self, ctx, id, value):
        self.isCorporate = False
        self.corporate.classes = ['col', 'hidden']
        self.corporateButton.set_style("background-color", "var(--background-secondary)")
        self.personalButton.set_style("background-color", "var(--ait)")
        self.vkn.value = ""
        self.companyName.value = ""
        self.taxOffice.value = ""
        self.eFatura.checkbox.value = False
        self.corporate.update()

    def corporate_click(self, ctx, id, value):
        self.isCorporate = True
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
            ctx.elements["myForm"].remove_class("turkey-address")
            ctx.elements["myForm"].add_class("default-address")
            self.turkey_addressFormat.add_class("hidden")
            self.default_addressFormat.remove_class("hidden")
            self.eFatura.style("display", "none")
            self.city.attrs["required"] = False
            self.region.attrs["required"] = False
            self.neighborhoods.input.attrs["required"] = False
            self.corporate.update()
            self.datalist_setter(self.country, value)
        else:
            ctx.elements["myForm"].remove_class("default-address")
            ctx.elements["myForm"].add_class("turkey-address")
            self.turkey_addressFormat.remove_class("hidden")
            self.default_addressFormat.add_class("hidden")
            self.eFatura.style("display", "flex")
            self.turkey_addressFormat.style("gap", "10px")
            self.city_datalist.input.attrs["required"] = True
            self.counties_datalist.input.attrs["required"] = True
            self.neighborhoods.input.attrs["required"] = True
            self.corporate.update()
            self.datalist_setter(self.country, value)

    def get_counties(self, ctx, id, value):
        value_=value.upper()
        self.city.value = value
        self.selected_city_counties = self.address_data.get(value_, [])
        countiesData = {key: key for key in self.selected_city_counties}
        content = ctx.elements["counties"]
        self.datalist_setter(self.city,value_)
        with content:
            self.counties = basic_datalist(name="", id="counties", placeholder=T("Select County"), required=True, options=countiesData, callback=self.get_neighborhoods)
        content.update()
        
    def get_neighborhoods(self, ctx, id, value):
        value_ = value.upper()
        if self.selected_city_counties != None:
            self.selected_city_neighborhoods = self.selected_city_counties.get(value_, [])
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
            "zipCode": self.zip_code.value,
            "country": self.country.value,
            "city": self.city.value,
            "county": self.counties_datalist.value,
            "region": self.region.value,
            "neighborhood": self.neighborhoods.value,
            "address_line_1": self.address_line1.value,
            "address_line_2": self.address_line2.value,
            "corporate": self.isCorporate,
            "vkn": self.vkn.value,
            "companyName": self.companyName.value,
            "taxOffice": self.taxOffice.value,
            "eFatura": self.eFatura.checkbox.value
        }
        if self.callback:
            self.callback(self, ctx, id, address_form_data)