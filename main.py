import sys
import token_gen
from googleapiclient.discovery import build
import update_courses
import drive_download
import os


def main():
    creds = token_gen.gen_token()
    classroom_service = build('classroom', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    if '-U' in sys.argv:
        new_courses = update_courses.update_course_list(classroom_service)
        update_courses.update_courseWorkMaterial(classroom_service, drive_service, new_courses)
        update_courses.update_course_announcements(classroom_service, drive_service, new_courses)
    announcement_token_file = open("./announcement_tokens.txt", "r+")
    announcement_token = announcement_token_file.readlines()
    courseWorkMaterial_token_file = open("./courseWorkMaterial_token.txt", "r+")
    courseWorkMaterial_token = courseWorkMaterial_token_file.readlines()
    with open("./course_list.txt", "r") as courses:
        course_line = courses.readlines()
        counter = 0
        for course in course_line:
            course_id = course.split()[0]
            course_name = course.split(" ", 1)[1].rsplit('\n')[0]
            announcement_info = classroom_service.courses().announcments().list(course_id,
                                                                                orderBy='updateTime asc',
                                                                                fields='announcements(text, '
                                                                                       'materials/driveFile'
                                                                                       '/driveFile(id,title)), '
                                                                                       'nextPageToken',
                                                                                pageSize=1,
                                                                                pageToken=announcement_token[
                                                                                    counter])
            while "nextPageToken" in announcement_info:
                announcement_token[counter] = announcement_info["nextPageToken"]
                announcement_info = classroom_service.courses().announcments().list(course_id,
                                                                                    orderBy='updateTime asc',
                                                                                    fields='announcements/(text, '
                                                                                           'materials/driveFile'
                                                                                           '/driveFile(id,title)), '
                                                                                           'nextPageToken',
                                                                                    pageSize=1,
                                                                                    pageToken=announcement_token[
                                                                                        counter])
                if "announcements" in announcement_info:
                    if "materials" in announcement_info['announcements'][0]:
                        for material in announcement_info['announcements'][0]['materials']:
                            file_id = material['driveFile']['driveFile']['id']
                            file_title = material['driveFile']['driveFile']['title']
                            drive_download.drive_dl(drive_service, file_id,
                                                    "/home/pratham/Classroom/" + course_name + "/update/announcements/" + file_title)
                    notif_title = "New Announcement"
                    notif_message = announcement_info['announcements'][0]['text']
                    notif = "notify-send " + notif_title + " " + notif_message
                    os.system(notif)
            courseWorkMaterial_info = classroom_service.courses().courseWorkMaterials().list(course_id,
                                                                                             orderBy='updateTime asc',
                                                                                             fields='courseWorkMaterials'
                                                                                                    '(title, '
                                                                                                    'materials/driveFile/'
                                                                                                    '/driveFile(id,title)), '
                                                                                                    'nextPageToken',
                                                                                             pageSize=1,
                                                                                             pageToken=
                                                                                             courseWorkMaterial_info[
                                                                                                 counter])
            while "nextPageToken" in courseWorkMaterial_info:
                courseWorkMaterial_token[counter] = courseWorkMaterial_info["nextPageToken"]
                courseWorkMaterial_info = classroom_service.courses().announcments().list(course_id,
                                                                                          orderBy='updateTime asc',
                                                                                          fields='courseWorkMaterials'
                                                                                                 '(title, '
                                                                                                 'materials/driveFile/'
                                                                                                 '/driveFile(id,'
                                                                                                 'title)), '
                                                                                                 'nextPageToken',
                                                                                          pageSize=1,
                                                                                          pageToken=announcement_token[
                                                                                              counter])
                if "courseWorkMaterial" in courseWorkMaterial_info:
                    if "materials" in courseWorkMaterial_info['courseWorkMaterials'][0]:
                        for material in announcement_info['courseWorkMaterials'][0]['materials']:
                            file_id = material['driveFile']['driveFile']['id']
                            file_title = material['driveFile']['driveFile']['title']
                            drive_download.drive_dl(drive_service, file_id,
                                                    "/home/pratham/Classroom/" + course_name + "/update"
                                                                                               "/courseWorkMaterials"
                                                                                               "/" + file_title)
                    notif.title = "New CourseWorkMaterial"
                    notif.message = courseWorkMaterial_info['courseWorkMaterials'][0]['title']
                    notif = "notify-send " + notif_title + " " + notif_message
                    os.system(notif)


if __name__ == '__main__':
    main()
