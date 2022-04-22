from pytube import YouTube
import getpass
import pathlib
import os
import ffmpeg
from termcolor import colored

# pytube için gerekli fonksiyonların tanımı
def on_complete(stream, filepath):
    print("İndirme tamamlandı.")
    print(f"Konum: {filepath}")


def on_progress(stream, chunks, bytes_remaining):
    loaded_size = f'{round(100 - (bytes_remaining / stream.filesize * 100), 2)}%'
    print(loaded_size)


def time(lenght):
    return (str(lenght // 60) + " dakika " + str(lenght % 60) + " saniye")


while True:
    try:
        video_link = input("İndirmek istediğin videonun linki: ")
        # Video bilgilerinin gösterilmesi
        print(f"İndirmek istediğin videonun linki {video_link} olarak ayarlandı.")
        print("-------------------------------------------------------------------")

        video_object = YouTube(video_link, on_complete_callback=on_complete, on_progress_callback=on_progress)

        print(colored(f"Videonun başlığı: {video_object.title}", 'red', attrs=['bold']))
        print(colored(f"Videonun sahibi: {video_object.author}", 'blue', attrs=['bold']))
        print(colored(f"Videonun süresi: {time(video_object.length)}", 'yellow', attrs=['bold']))
        print(colored(f"Videonun izlenme sayısı: {video_object.views} kez izlendi", 'magenta', attrs=['bold']))
        print("-------------------------------------------------------------------")

        # Videonun indirilmesi
        print("Video(mp4) indirmek için : 1\nSadece ses(mp3) indirmek için : 2\n1080p indir (Optimize değil)"
              " : 3\nMevcut işlemi iptal etmek için : 4\nÇıkış için : 5")
        download_option = input("İşlem seçiniz: ")
        '''
        #Eğer indirme konumunu indirilenler klasörü olması gerekliyse...
        #if not download_option == "4":
            #username = getpass.getuser()
            #download_location = pathlib.Path("C://Users//" + username + "//Downloads")
        '''
        match download_option:
            case "1":
                gonna_download = video_object.streams.get_highest_resolution()
                gonna_download.download()
            case "2":
                gonna_download = video_object.streams.get_by_itag(251)
                out_file = gonna_download.download()
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            case "3":
                onaylama = input("Uyarı: Bu işlem yüksek miktarda işlemci yükü gerektirebilir ve uzun sürebilir?"
                      "Devam etmek istiyor musun? Y/n (Varsayılan: n) = ")
                if onaylama == "Y":
                    try:
                        gonna_download_video = video_object.streams.filter(resolution="1080p").first().download()
                        gonna_download_audio = video_object.streams.get_by_itag(251)
                        out_file = gonna_download_audio.download()
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file)
                        # Dosyaların birleştirilmesi
                        infile1 = ffmpeg.input(video_object.title + ".mp4")
                        infile2 = ffmpeg.input(video_object.title + ".mp3")
                        output_file_name = video_object.title + "_merged.mp4"
                        merged = ffmpeg.concat(infile1, infile2, v=1, a=1).output('./' + output_file_name).run()
                        # Ayrılmış durumdaki ses ve görüntünün silinmesi
                        if os.path.exists(video_object.title + ".mp4"):
                            os.remove(video_object.title + ".mp4")
                        else:
                            print("Dosya mevcut değil")
                        if os.path.exists(video_object.title + ".mp3"):
                            os.remove(video_object.title + ".mp3")
                        else:
                            print("Dosya mevcut değil")
                    except:
                        print("Bir şeyler ters gitti. Videonun 1080p çözünürlüğe sahip olduğuna emin ol.")
                else:
                    print("Vazgeçtiniz.")
                    pass
            case "4":
                print("Mevcut işlemi yapmaktan vazgeçtiniz.")
                pass
            case "5":
                print("İndirici kapatılıyor...")
                break
    except KeyboardInterrupt:
        print("\nİndirici kapatılıyor...")
        exit()
    except:
        print("Bir şeyler ters gitti.")

