#-------------------------------------------------------------------------------
 #!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
import os
from PySide2.QtGui import QPixmap, QIcon

def Icon(icon):
    path = os.path.dirname(os.path.realpath(__file__))
    icon = os.path.normpath(os.path.join(path, 'images', icon))
    return QIcon(QPixmap(icon + '.png'))

def Image(icon):
    path = os.path.dirname(os.path.realpath(__file__))
    icon = os.path.normpath(os.path.join(path, 'images', icon))
    return QPixmap(icon + '.png')

class photoscan:
    CHUNCK_16 = r'photoscan/CHUNCK_16'
    CHUNCK_32 = r'photoscan/CHUNCK_32'
    ADD_CAMERA_GROUP_16 = r'photoscan/ADD_CAMERA_GROUP_16'
    ADD_CAMERA_GROUP_32 = r'photoscan/ADD_CAMERA_GROUP_32'
    ADD_CHUNK_16 = r'photoscan/ADD_CHUNK_16'
    ADD_CHUNK_32 = r'photoscan/ADD_CHUNK_32'
    ADD_FOLDER_16 = r'photoscan/ADD_FOLDER_16'
    ADD_FOLDER_32 = r'photoscan/ADD_FOLDER_32'
    ADD_FRAMES_16 = r'photoscan/ADD_FRAMES_16'
    ADD_FRAMES_32 = r'photoscan/ADD_FRAMES_32'
    ADD_MARKER_16 = r'photoscan/ADD_MARKER_16'
    ADD_MARKER_32 = r'photoscan/ADD_MARKER_32'
    ADD_PHOTOS_16 = r'photoscan/ADD_PHOTOS_16'
    ADD_PHOTOS_32 = r'photoscan/ADD_PHOTOS_32'
    ADD_SCALE_BAR_16 = r'photoscan/ADD_SCALE_BAR_16'
    ADD_SCALE_BAR_32 = r'photoscan/ADD_SCALE_BAR_32'
    ADD_SHAPE_LAYER_16 = r'photoscan/ADD_SHAPE_LAYER_16'
    ADD_SHAPE_LAYER_32 = r'photoscan/ADD_SHAPE_LAYER_32'
    ARROW_DOWN_16 = r'photoscan/ARROW_DOWN_16'
    ARROW_DOWN_32 = r'photoscan/ARROW_DOWN_32'
    CAMERA_16 = r'photoscan/CAMERA_16'
    CAMERA_32 = r'photoscan/CAMERA_32'
    CLEAR_LOG_16 = r'photoscan/CLEAR_LOG_16'
    CLEAR_LOG_32 = r'photoscan/CLEAR_LOG_32'
    CONSOLE_16 = r'photoscan/CONSOLE_16'
    CONSOLE_32 = r'photoscan/CONSOLE_32'
    CONVERT_16 = r'photoscan/CONVERT_16'
    CONVERT_32 = r'photoscan/CONVERT_32'
    CROP_SELECTION_16 = r'photoscan/CROP_SELECTION_16'
    CROP_SELECTION_32 = r'photoscan/CROP_SELECTION_32'
    DECREASE_BRIGHTNESS_16 = r'photoscan/DECREASE_BRIGHTNESS_16'
    DECREASE_BRIGHTNESS_32 = r'photoscan/DECREASE_BRIGHTNESS_32'
    DENSE_CLOUD_16 = r'photoscan/DENSE_CLOUD_16'
    DENSE_CLOUD_32 = r'photoscan/DENSE_CLOUD_32'
    DENSE_CLOUD_CLASSES_16 = r'photoscan/DENSE_CLOUD_CLASSES_16'
    DENSE_CLOUD_CLASSES_32 = r'photoscan/DENSE_CLOUD_CLASSES_32'
    DETAILS_16 = r'photoscan/DETAILS_16'
    DETAILS_32 = r'photoscan/DETAILS_32'
    DISABLE_16 = r'photoscan/DISABLE_16'
    DISABLE_32 = r'photoscan/DISABLE_32'
    DRAW_POLYLINE_16 = r'photoscan/DRAW_POLYLINE_16'
    DRAW_POLYLINE_32 = r'photoscan/DRAW_POLYLINE_32'
    DUPLICATE_16 = r'photoscan/DUPLICATE_16'
    DUPLICATE_32 = r'photoscan/DUPLICATE_32'
    ENABLE_16 = r'photoscan/ENABLE_16'
    ENABLE_32 = r'photoscan/ENABLE_32'
    EXPORT_16 = r'photoscan/EXPORT_16'
    EXPORT_32 = r'photoscan/EXPORT_32'
    FILTER_PHOTOS_BY_CAMERAS_16 = r'photoscan/FILTER_PHOTOS_BY_CAMERAS_16'
    FILTER_PHOTOS_BY_CAMERAS_32 = r'photoscan/FILTER_PHOTOS_BY_CAMERAS_32'
    FILTER_PHOTOS_BY_MARKERS_16 = r'photoscan/FILTER_PHOTOS_BY_MARKERS_16'
    FILTER_PHOTOS_BY_MARKERS_32 = r'photoscan/FILTER_PHOTOS_BY_MARKERS_32'
    FILTER_PHOTOS_BY_POINT_16 = r'photoscan/FILTER_PHOTOS_BY_POINT_16'
    FILTER_PHOTOS_BY_POINT_32 = r'photoscan/FILTER_PHOTOS_BY_POINT_32'
    FILTER_PHOTOS_BY_SHAPES_16 = r'photoscan/FILTER_PHOTOS_BY_SHAPES_16'
    FILTER_PHOTOS_BY_SHAPES_32 = r'photoscan/FILTER_PHOTOS_BY_SHAPES_32'
    FILTER_PHOTOS_BY_TIE_POINTS_16 = r'photoscan/FILTER_PHOTOS_BY_TIE_POINTS_16'
    FILTER_PHOTOS_BY_TIE_POINTS_32 = r'photoscan/FILTER_PHOTOS_BY_TIE_POINTS_32'
    IMPORT_16 = r'photoscan/IMPORT_16'
    IMPORT_32 = r'photoscan/IMPORT_32'
    IMPORT_EXIF_16 = r'photoscan/IMPORT_EXIF_16'
    IMPORT_EXIF_32 = r'photoscan/IMPORT_EXIF_32'
    INCREASE_BRIGHTNESS_16 = r'photoscan/INCREASE_BRIGHTNESS_16'
    INCREASE_BRIGHTNESS_32 = r'photoscan/INCREASE_BRIGHTNESS_32'
    JOBS_16 = r'photoscan/JOBS_16'
    JOBS_32 = r'photoscan/JOBS_32'
    LARGE_16 = r'photoscan/LARGE_16'
    LARGE_32 = r'photoscan/LARGE_32'
    MOVE_REGION_16 = r'photoscan/MOVE_REGION_16'
    MOVE_REGION_32 = r'photoscan/MOVE_REGION_32'
    NAVIGATION_16 = r'photoscan/NAVIGATION_16'
    NAVIGATION_32 = r'photoscan/NAVIGATION_32'
    BLANK_16 = r'photoscan/BLANK_16'
    BLANK_32 = r'photoscan/BLANK_32'
    NEW_CHUNK_16 = r'photoscan/NEW_CHUNK_16'
    FOLDER_16 = r'photoscan/FOLDER_16'
    FOLDER_32 = r'photoscan/FOLDER_32'
    OPTIMIZE_CAMERAS_16 = r'photoscan/OPTIMIZE_CAMERAS_16'
    OPTIMIZE_CAMERAS_32 = r'photoscan/OPTIMIZE_CAMERAS_32'
    PHOTOS_16 = r'photoscan/PHOTOS_16'
    PHOTOS_32 = r'photoscan/PHOTOS_32'
    PLAY_16 = r'photoscan/PLAY_16'
    PLAY_32 = r'photoscan/PLAY_32'
    POINT_CLOUD_16 = r'photoscan/POINT_CLOUD_16'
    POINT_CLOUD_32 = r'photoscan/POINT_CLOUD_32'
    RECTANGLE_SELECTION_16 = r'photoscan/RECTANGLE_SELECTION_16'
    RECTANGLE_SELECTION_32 = r'photoscan/RECTANGLE_SELECTION_32'
    REDO_16 = r'photoscan/REDO_16'
    REDO_32 = r'photoscan/REDO_32'
    REFERENCE_16 = r'photoscan/REFERENCE_16'
    REFERENCE_32 = r'photoscan/REFERENCE_32'
    REMOVE_16 = r'photoscan/REMOVE_16'
    REMOVE_32 = r'photoscan/REMOVE_32'
    REMOVE_FRAMES_16 = r'photoscan/REMOVE_FRAMES_16'
    REMOVE_FRAMES_32 = r'photoscan/REMOVE_FRAMES_32'
    RENAME_16 = r'photoscan/RENAME_16'
    RENAME_32 = r'photoscan/RENAME_32'
    RESET_FILTER_16 = r'photoscan/RESET_FILTER_16'
    RESET_FILTER_32 = r'photoscan/RESET_FILTER_32'
    RESET_VIEW_16 = r'photoscan/RESET_VIEW_16'
    RESET_VIEW_32 = r'photoscan/RESET_VIEW_32'
    ROTATE_LEFT_16 = r'photoscan/ROTATE_LEFT_16'
    ROTATE_LEFT_32 = r'photoscan/ROTATE_LEFT_32'
    ROTATE_RIGHT_16 = r'photoscan/ROTATE_RIGHT_16'
    ROTATE_RIGHT_32 = r'photoscan/ROTATE_RIGHT_32'
    RULER_16 = r'photoscan/RULER_16'
    RULER_32 = r'photoscan/RULER_32'
    SAVE_16 = r'photoscan/SAVE_16'
    SAVE_32 = r'photoscan/SAVE_32'
    SETTINGS_16 = r'photoscan/SETTINGS_16'
    SETTINGS_32 = r'photoscan/SETTINGS_32'
    SET_ACTIVE_16 = r'photoscan/SET_ACTIVE_16'
    SET_ACTIVE_32 = r'photoscan/SET_ACTIVE_32'
    SET_BRIGHTNESS_16 = r'photoscan/SET_BRIGHTNESS_16'
    SET_BRIGHTNESS_32 = r'photoscan/SET_BRIGHTNESS_32'
    SET_PALETTE_16 = r'photoscan/SET_PALETTE_16'
    SET_PALETTE_32 = r'photoscan/SET_PALETTE_32'
    SHADED_16 = r'photoscan/SHADED_16'
    SHADED_32 = r'photoscan/SHADED_32'
    SHOW_ALIGNED_CHUNKS_16 = r'photoscan/SHOW_ALIGNED_CHUNKS_16'
    SHOW_ALIGNED_CHUNKS_32 = r'photoscan/SHOW_ALIGNED_CHUNKS_32'
    SHOW_DEPTH_MAPS_16 = r'photoscan/SHOW_DEPTH_MAPS_16'
    SHOW_DEPTH_MAPS_32 = r'photoscan/SHOW_DEPTH_MAPS_32'
    SHOW_IMAGES_16 = r'photoscan/SHOW_IMAGES_16'
    SHOW_IMAGES_32 = r'photoscan/SHOW_IMAGES_32'
    SHOW_INFO_16 = r'photoscan/SHOW_INFO_16'
    SHOW_INFO_32 = r'photoscan/SHOW_INFO_32'
    SHOW_MASKS_16 = r'photoscan/SHOW_MASKS_16'
    SHOW_MASKS_32 = r'photoscan/SHOW_MASKS_32'
    SHOW_SHAPES_16 = r'photoscan/SHOW_SHAPES_16'
    SHOW_SHAPES_32 = r'photoscan/SHOW_SHAPES_32'
    SMALL_16 = r'photoscan/SMALL_16'
    SMALL_32 = r'photoscan/SMALL_32'
    SOLID_16 = r'photoscan/SOLID_16'
    SOLID_32 = r'photoscan/SOLID_32'
    STOP_16 = r'photoscan/STOP_16'
    STOP_32 = r'photoscan/STOP_32'
    TEXTURED_16 = r'photoscan/TEXTURED_16'
    TEXTURED_32 = r'photoscan/TEXTURED_32'
    TILED_MODEL_16 = r'photoscan/TILED_MODEL_16'
    TILED_MODEL_32 = r'photoscan/TILED_MODEL_32'
    TIMELINE_16 = r'photoscan/TIMELINE_16'
    TIMELINE_32 = r'photoscan/TIMELINE_32'
    UNDO_16 = r'photoscan/UNDO_16'
    UNDO_32 = r'photoscan/UNDO_32'
    UPDATE_16 = r'photoscan/UPDATE_16'
    UPDATE_32 = r'photoscan/UPDATE_32'
    VIEW_ERRORS_16 = r'photoscan/VIEW_ERRORS_16'
    VIEW_ERRORS_32 = r'photoscan/VIEW_ERRORS_32'
    VIEW_ESTIMATED_16 = r'photoscan/VIEW_ESTIMATED_16'
    VIEW_ESTIMATED_32 = r'photoscan/VIEW_ESTIMATED_32'
    VIEW_SOURCE_16 = r'photoscan/VIEW_SOURCE_16'
    VIEW_SOURCE_32 = r'photoscan/VIEW_SOURCE_32'
    WIREFRAME_16 = r'photoscan/WIREFRAME_16'
    WIREFRAME_32 = r'photoscan/WIREFRAME_32'
    WORKSPACE_16 = r'photoscan/WORKSPACE_16'
    WORKSPACE_32 = r'photoscan/WORKSPACE_32'
    WTF_8 = r'photoscan/WTF_8'
    ZOOM_IN_16 = r'photoscan/ZOOM_IN_16'
    ZOOM_IN_32 = r'photoscan/ZOOM_IN_32'
    ZOOM_OUT_16 = r'photoscan/ZOOM_OUT_16'
    ZOOM_OUT_32 = r'photoscan/ZOOM_OUT_32'

class ssciph:
    CROSS_16 = r'ssciph/CROSS_16'
    CROSS_32 = r'ssciph/CROSS_32'
    PLUS_16 = r'ssciph/PLUS_16'
    PLUS_32 = r'ssciph/PLUS_32'
    XY_16 = r'ssciph/XY_16'
    XY_32 = r'ssciph/XY_32'
    TICK_16 = r'ssciph/TICK_16'
    TICK_32 = r'ssciph/TICK_32'
    FIRST_16 = r'ssciph/FIRST_16'
    FIRST_32 = r'ssciph/FIRST_32'
    LAST_16 = r'ssciph/LAST_16'
    LAST_32 = r'ssciph/LAST_32'
    RIGHT_16 = r'ssciph/RIGHT_16'
    RIGHT_32 = r'ssciph/RIGHT_32'
    LEFT_16 = r'ssciph/LEFT_16'
    LEFT_32 = r'ssciph/LEFT_32'

class JOG:
    JOGm1_32 = r'jog/JOGm1_32'
    JOGm10_32 = r'jog/JOGm10_32'
    JOGm100_32 = r'jog/JOGm100_32'
    JOGp1_32 = r'jog/JOGp1_32'
    JOGp10_32 = r'jog/JOGp10_32'
    JOGp100_32 = r'jog/JOGp100_32'


class resources:

    GREEN_INDICATOR = 'indicator/g'
    GREY_INDICATOR = 'indicator/grey'
    RED_INDICATOR = 'indicator/r'
    YELLOW_INDICATOR = 'indicator/y'



