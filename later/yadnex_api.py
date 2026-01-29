# client.accountSettings()
# client.account_status()
# print(client.albums_with_tracks(5535519))
# client.artists_tracks(id)
# client.chart(chart_option='place')
# client.feed()
# client.account_settings_set()

# with open('data.json', 'w') as f:
#     f.write(json.dumps(client.albums_with_tracks(5535519).to_json()))

###### ШТУКА ДЛЯ ЗАГРУЗКИ И УДАЛЕНИЯ ФАЙЛОВ НА ДИСКЕ #######
# def download_track_by_id(id: int):
#     track = client.tracks(id)[0]
#     track_download_info = track.get_download_info(1)[0]
#     urllib.request.urlretrieve(track_download_info['direct_link'], f'{track.id}.{track_download_info['codec']}')
# def delete_track_by_id(id: int):
#     file = Path(f'{id}.mp3')
#     if file.exists():
#         file.unlink()