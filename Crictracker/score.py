from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import requests
import re



class CricketScore:
    #constructor
    def __init__(self, rootWindow):
        self.rootWindow = rootWindow
        self.rootWindow.title('Live Cricket Score')
        self.rootWindow.geometry('650x350')
        self.bg = ImageTk.PhotoImage(file = "cricket.jpg")
        bg = Label(self.rootWindow, image=self.bg).place(x=0, y=0)



#lets give a Label to my GUI
        self.label = Label(self.rootWindow, text='Live Matches', font=("times new roman", 40), compound='center').pack(padx=100, pady=50)


#fetch the live match details and set in my GUI
        self.var = StringVar()
        self.matches = self.match_details()
        self.data = [i for i in self.matches.keys()]
        self.cb = Combobox(self.rootWindow, values=self.data, width = 50)
        self.cb.place(x = 250, y= 200)


        self.b1 = Button(self.rootWindow, text = "Check Score", font=("times new roman",15), command=self.show_match_details).place(x=80, y=190)


        #creating command for the check score button
    def select(self):
        return self.cb.get()

    def show_match_details(self):
        self.frame1 = Frame(self.rootWindow, bg = "#ADD8E6")
        self.frame1.place(x=180,y=280,width=600,height=200)
        #fetching details of the match
        x = self.matches[self.select()]

        #displaying team names
        Label(self.frame1, text = self.select()+ " - " + x['match_header'], font=("times new roman",15,"bold"), bg = "#ADD8E6",fg ="black" , bd=0).place(x=150, y=15)


        Label(self.frame1, text =  "Score Details : ", font=("times new roman",10,"bold"), bg = "#ADD8E6",fg="black" ,bd=0).place(x=10, y=40)
        Label(self.frame1, text =  x['score_card'], font=("times new roman",10,"bold"), bg = "#ADD8E6", fg="black",bd=0).place(x=20, y=60)
        Label(self.frame1, text = "Summary : ", font=("times new roman",10,"bold"), bg = "#ADD8E6", fg="black",bd=0).place(x=10, y=100)
        Label(self.frame1, text =  x['summary'], font=("times new roman",10,"bold"), bg = "#ADD8E6", fg="black",bd=0).place(x=20, y=120)








#will load all the matches details
    def match_details(self):
#to scrap the data
        details=self.scrap()
# need to parse and read the relevant data  

        live_match={}
        for detail in details :
            live_team_details = {}
            summary = self.match_summary(detail)
           # print(summary)
            if summary is not None :
                match_header = self.match_header(detail).text
                teams = self.teams_name(detail)
                score_card = self.team_score(detail)
                live_team_details['summary'] = summary.text
                live_team_details['match_header'] = match_header
                live_team_details['score_card'] = score_card[0] + " :: "+score_card[1]  
                live_match[teams[0] + " vs "+ teams[1]] = live_team_details
        return live_match

#function to fetch the team score
    def team_score(self, detail):
        t = []
        team1_details = detail.find("div", class_="cb-hmscg-bat-txt").text
        team2_details = detail.find("div", class_="cb-hmscg-bwl-txt").text
        t.append(team1_details)
        t.append(team2_details)
        return t


#function to fetch the teamname
    def teams_name(self,detail):
        t = []
        team1_details = detail.find("div", class_="cb-hmscg-bat-txt").text
        team1_index = re.search(r"\d",team1_details).start() if re.search(r"\d", team1_details) else len(team1_details)
        team2_details = detail.find("div", class_="cb-hmscg-bwl-txt").text
        team2_index = re.search(r"\d",team2_details).start() if re.search(r"\d", team2_details) else len(team2_details)
        t.append(team1_details[:team1_index])
        t.append(team2_details[:team2_index])
        return t

#function to fetch a given summary
    def match_summary(self, detail):
        return detail.find("div", class_="cb-mtch-crd-state")

    def match_header(self, detail):
        return detail.find("div", class_="cb-mtch-crd-hdr")


##function to scrap the website
    def scrap(self):
        URL = "https://www.cricbuzz.com/"
        page = requests.get(URL)
#parse the response and fetch the relevant data
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="match_menu_container")
        scrap_results = results.find_all("li", class_= "cb-match-card")
        return scrap_results
    
        #button to check the details of the match


def main():
    #start the GUI window
    rootWindow = Tk()

    #fetch the cricket score
    obj = CricketScore(rootWindow)
    #keep on diplaying the gui to fetch the live updates
    rootWindow.mainloop()


    #execute
if __name__=='__main__':
     main()
