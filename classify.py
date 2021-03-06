import os, shutil
from exifio import *
from rename import *
from PIL.ExifTags import TAGS


# AAEについてのみ別処理を追加


# リストで渡された全ファイルをdest_dir以下に撮影日時毎に分類する (デフォルトでムーブ)
def cls_by_dt_original(fpath_list, dest_dir, cls_mode, move=True):

    for fpath in fpath_list:
        dpath, fname, ext = split_fpath(fpath)
        tags = get_exif(fpath)
        dtstr = str(get_val_from_tags(tags, 'EXIF DateTimeOriginal'))
        dname = 'Unknown'
        
        # 撮影日時から移動先フォルダ名を生成
        if dtstr != 'None':
            if cls_mode == 'year':
                dname = dtstr.split(':')[0]
            elif cls_mode == 'month':
                dname = dtstr.split(':')[1]
            elif cls_mode == 'day':
                dname = dtstr.split(':')[2][:2]
            else:
                print('ERROR : unmatched cls_mode')
                sys.exit()
        
        dt_dir = os.path.join(dest_dir, dname)
        
        if not os.path.exists(dt_dir):
            os.mkdir(dt_dir)
            print('DIR_CREATED : new directory [', dt_dir, '] was created')


        dest_path = os.path.join(dt_dir, fname + '.' + ext)  # ムーブ先のパスを生成

        if move:
            shutil.move(fpath, dest_path)                # ムーブを実行
            print('FILE_MOVED : file [', fpath, '] was moved to [', dest_path, ']')
        else:                             
            shutil.copy2(fpath, dest_path)               # コピーを実行
            print('FILE_COPIED : file [', fpath, '] was copied to [', dest_path, ']')


# リストで渡された全ファイルをdest_dir以下に拡張子毎に分類する (デフォルトでムーブ)
def cls_by_ext(fpath_list, dest_dir, move=True, jpeg2jpg=True):

    for fpath in fpath_list:
        _, fname, ext = split_fpath(fpath)
        ext_dir = ext.upper()  # 拡張子を大文字としたフォルダ名にする

        if jpeg2jpg:  # JPGとJPEGを統一する
            if ext_dir == 'JPEG':
                ext_dir = 'JPG'

        ext_dir = os.path.join(dest_dir, ext_dir)  # 各拡張子でフォルダを作成

        if not os.path.exists(ext_dir):        # 拡張子のフォルダが存在しなければ新規作成
            os.mkdir(ext_dir)
            print('DIR_CREATED : new directory [', ext_dir, '] was created')

        dest_path = os.path.join(ext_dir, fname + '.' + ext)  # ムーブ先のパスを生成

        if move:
            shutil.move(fpath, dest_path)                # ムーブを実行
            print('FILE_MOVED : file [', fpath, '] was moved to [', dest_path, ']')
        else:                             
            shutil.copy2(fpath, dest_path)               # コピーを実行
            print('FILE_COPIED : file [', fpath, '] was copied to [', dest_path, ']')



# リストで渡された全ファイルをexif情報ごとにフォルダ分けする (デフォルトでムーブ)
def cls_by_exif(fpath_list, dest_dir, exif_name, move=True):

    for fpath in fpath_list:
        tags = get_exif(fpath)
        tag_val = get_val_from_tags(tags, exif_name)       # タグ情報を取得

        if not tag_val:                                    # 対応するexif情報なし
            tag_val = 'Unknown'
            print('UNKNOWN_VALUE : file [', fpath , '] has no value of', exif_name)

        tag_val_dir = os.path.join(dest_dir, str(tag_val))   # タグ情報をディレクトリ名とする
        
        if not os.path.exists(tag_val_dir):             # タグ情報のフォルダが存在しなければ新規作成
            os.mkdir(tag_val_dir)
            print('DIR_CREATED : new directory [', tag_val_dir, '] was created')

        _, fname, ext = split_fpath(fpath)
        dest_path = os.path.join(tag_val_dir, fname + '.' + ext)  # 処理後のパスを生成
       
        if move:
            shutil.move(fpath, dest_path)                # ムーブを実行
            print('FILE_MOVED : file [', fpath, '] was moved to [', dest_path, ']')
        else:                             
            shutil.copy2(fpath, dest_path)               # コピーを実行
            print('FILE_COPIED : file [', fpath, '] was copied to [', dest_path, ']')
