#!/usr/bin/env python3

import csv

INDEX_TEMPLATE = 'src/index_template.html'
TABLE = 'table.csv'
ACCOUNTS='accounts.csv'
REFERENCES = 'references.csv'
STATE_TO_EMOJI_MAP = {
	"FULL_MIGRATION": "✨",
	"HALF_MIGRATION": "⭐️",
	"ACCOUNT_OPENED": "🔒"
}

def generate_table():
	table = "<table>"
	table += "<tr><th>📜</th><th>Nombre</th><th>Cuenta</th><th>Descripción</th><th>Fuente</th></tr>"
	with open(TABLE, newline='') as csvfile:
		rows = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for row in rows:
			table += generate_table_row(row)
	table += "</table>"
	return table

def generate_table_row(data):
	row = "<tr>"
	name, description, web_link, state = list(data.values())

	row += '<td>%s</td>' % (STATE_TO_EMOJI_MAP[state])
	row += '<td><a href="%s">%s</a></td>' % (web_link, name)
	row += '<td>%s</td>' % (generate_account_list_for(name))
	row += '<td>%s</td>' % (description)
	row += '<td>%s</td>' % (generate_reference_list_for(name))

	return row + "</tr>"

def generate_reference_list_for(current_name):
	ref_list = "<ul>"
	with open(REFERENCES, newline='') as csvfile:
		rows = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for row in rows:
			name,link,text = list(row.values())
			if name == current_name:
				ref_list += '<li><a href="%s">%s</li>' % (link, text)
	ref_list += "</ul>"
	return ref_list


def generate_account_list_for(current_name):
	ref_list = "<ul>"
	with open(ACCOUNTS, newline='') as csvfile:
		rows = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for row in rows:
			name,username,server = list(row.values())
			if name == current_name:
				link_resolver = UserProfileLinkResolverFactory().create(server)
				link = link_resolver.get_user_profile_link_from_username(username)
				ref_list += '<li class="account"><a href="%s"><img src="./images/%s.svg" height="20"><p>%s</p></li>' % (link, server, username)
	ref_list += "</ul>"
	return ref_list

def main():
	with open(INDEX_TEMPLATE) as file:
		index = file.read()
		index = index.replace("${TABLE}", generate_table())
		print(index)


class UserProfileLinkResolverFactory(object):
	def create(self, server):
		if server in ("Akkoma", "Pleroma"):
			return PleromaUserProfileLinkResolver()
		else:
			return UserProfileLinkResolver()

class UserProfileLinkResolver(object):
	def get_user_profile_link_from_username(self, username):
		_,name,domain = username.split("@")
		link = "https://%s/@%s" % (domain, name)
		return link

class PleromaUserProfileLinkResolver(object):
	def get_user_profile_link_from_username(self, username):
		_,name,domain = username.split("@")
		link = "https://%s/%s" % (domain, name)
		return link

main()
