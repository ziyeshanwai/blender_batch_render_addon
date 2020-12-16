bl_info = {
    "name": "Batch Export",
    "author": "wangliyou",
    "version": (1, 2),
    "blender": (2, 83, 0),
    "location": "View3D > Toolbar > Batch Export",
    "description": "batch export abc or video",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}
 
import bpy
import os
 
 
    #This is the Main Panel (Parent of Panel A and B)
class MAINUI(bpy.types.Panel):
    bl_label = "Batch Export Tool"
    bl_idname = "VIEW_PT_MainUI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Batch Export'
   
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text= "Batch ExPORT TOOL", icon= 'OBJECT_ORIGIN')
        row = layout.row()
        row.operator("wm.batch_render", icon= 'CUBE', text= "batch render aifa animaition")
        row = layout.row()
        row.operator("wm.batch_render_bone_animation", icon= 'CUBE', text= "batch render bone animaition")
        row = layout.row()
        row.operator("wm.batch_export_abc", icon= 'CUBE', text= "batch export abc")
        
        
class WM_OT_batch_export_abc(bpy.types.Operator):
    
    bl_label = "batch export abc box"
    bl_idname = "wm.batch_export_abc"
    
    input_dir = bpy.props.StringProperty(name= "input dir", default= "")
    output_dir = bpy.props.StringProperty(name= "output dir:", default= "")
    scale = bpy.props.FloatProperty(name="scale", description="scale", default=1.0, min=0.01, max=100.0)
    
    def execute(self, context):
        
        input_dir = self.input_dir
        print("input_dir is {}".format(input_dir))
        output_dir = self.output_dir
        print("output_dir is {}".format(output_dir))
        names = os.listdir(input_dir)
        names = list(filter(lambda x: x.endswith(".fbx"), names))
        number = 0
        for name in names:
            input_path = os.path.join(input_dir, name)
            self.import_fbx(input_path)
            output_path = os.path.join(output_dir, name[:-3]+'abc')
            self.export(output_path)
            print("-" * 100)
            number += 1
            print("{} export finish".format(name))
            print("{}/{}".format(number, len(names)))
        return {'FINISHED'}
    
    def invoke(self, context, event):
       
        return context.window_manager.invoke_props_dialog(self)
    
    def set_frame_number(self):
        start_number = bpy.data.objects['head_geo'].animation_data.action.frame_range[0]
        end_number = bpy.data.objects['head_geo'].animation_data.action.frame_range[1]
        bpy.context.scene.frame_start = start_number
        bpy.context.scene.frame_end = end_number
        
    def import_fbx(self, file):
        bpy.ops.import_scene.fbx(filepath=file, global_scale=self.scale) # bas
        bpy.context.selected_objects[0].name ='head_geo'
        
    def export(self, output_path):
        
        for i in range(1, len(bpy.data.objects['head_geo'].data.shape_keys.key_blocks)):
            bpy.data.objects['head_geo'].data.shape_keys.key_blocks[i].slider_min = -5
            bpy.data.objects['head_geo'].data.shape_keys.key_blocks[i].slider_max = 5
        self.set_frame_number()
        bpy.data.objects['head_geo'].select_set(True)
        bpy.ops.wm.alembic_export(filepath=output_path, selected=True)
        bpy.ops.object.delete(use_global=False)
        print("export {}".format(output_path))
        
 
class WM_OT_batch_render(bpy.types.Operator):
    
    bl_label = "batch export render box"
    bl_idname = "wm.batch_render"
   
    input_dir = bpy.props.StringProperty(name= "input dir", default= "")
    output_dir = bpy.props.StringProperty(name= "output dir:", default= "")
    
    def execute(self, context):
       
        input_dir = self.input_dir
        print("input_dir is {}".format(input_dir))
        output_dir = self.output_dir
        print("output_dir is {}".format(output_dir))
        self.ini_render_settings()
        names = os.listdir(input_dir)
        names = list(filter(lambda x: x.endswith(".fbx"), names))
        number = 0
        for name in names:
            input_path = os.path.join(input_dir, name)
            self.import_fbx(input_path)
            output_path = os.path.join(output_dir, name[:-3]+'mp4')
            self.render_animation(output_path)
            number += 1
            print("-" * 100)
            print("{} render finish".format(name))
            print("{}/{}".format(number, len(names)))
       
        return {'FINISHED'}
   
    def invoke(self, context, event):
       
        return context.window_manager.invoke_props_dialog(self)
 
    def ini_render_settings(self):
        print("initial render setting")
        bpy.context.scene.unit_settings.scale_length = 0.01
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.fps = 60

    
    def set_frame_number(self):
        start_number = bpy.data.objects['head_geo'].animation_data.action.frame_range[0]
        end_number = bpy.data.objects['head_geo'].animation_data.action.frame_range[1]
        bpy.context.scene.frame_start = start_number
        bpy.context.scene.frame_end = end_number
         
    def adjust_view(self):
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break
        space = area.spaces[0]
        context = bpy.context.copy()
        context['area'] = area
        context['region'] = region
        context['space_data'] = space
        bpy.data.objects['head_geo'].select_set(True)
        bpy.ops.view3d.view_selected(context)
        bpy.ops.view3d.view_axis(context, type='FRONT')
        context['space_data'].overlay.show_overlays = False

    def render_animation(self, output_path):
        
        for i in range(1, len(bpy.data.objects['head_geo'].data.shape_keys.key_blocks)):
            bpy.data.objects['head_geo'].data.shape_keys.key_blocks[i].slider_min = -5
            bpy.data.objects['head_geo'].data.shape_keys.key_blocks[i].slider_max = 5
        self.set_frame_number()
        bpy.context.scene.render.filepath = output_path
        self.adjust_view()
        bpy.ops.render.opengl(animation=True)
        bpy.data.objects['head_geo'].select_set(True)
        bpy.ops.object.delete(use_global=False)


    def import_fbx(self, file):
        bpy.ops.import_scene.fbx(filepath=file, global_scale=0.01) # bas
        bpy.context.selected_objects[0].name ='head_geo'
 
        
class WM_OT_batch_render_bone_animation(bpy.types.Operator):
    
    bl_label = "batch export render box"
    bl_idname = "wm.batch_render_bone_animation"
   
    input_dir = bpy.props.StringProperty(name= "input dir", default= "")
    output_dir = bpy.props.StringProperty(name= "output dir:", default= "")
    
    def execute(self, context):
       
        input_dir = self.input_dir
        print("input_dir is {}".format(input_dir))
        output_dir = self.output_dir
        print("output_dir is {}".format(output_dir))
        self.ini_render_settings()
        names = os.listdir(input_dir)
        names = list(filter(lambda x: x.endswith(".fbx"), names))
        number = 0
        for name in names:
            input_path = os.path.join(input_dir, name)
            self.import_fbx(input_path)
            output_path = os.path.join(output_dir, name[:-3]+'mp4')
            self.render_animation(output_path)
            number += 1
            print("-" * 100)
            print("{} render finish".format(name))
            print("{}/{}".format(number, len(names)))
       
        return {'FINISHED'}
   
    def invoke(self, context, event):
       
        return context.window_manager.invoke_props_dialog(self)
 
    def ini_render_settings(self):
        print("initial render setting")
        bpy.context.scene.unit_settings.scale_length = 0.01
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.fps = 60

    
    def set_frame_number(self):
        start_number = bpy.data.objects['head_geo_rig'].animation_data.action.frame_range[0]
        end_number = bpy.data.objects['head_geo_rig'].animation_data.action.frame_range[1]
        bpy.context.scene.frame_start = start_number
        bpy.context.scene.frame_end = end_number
         
    def adjust_view(self):
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break
        space = area.spaces[0]
        context = bpy.context.copy()
        context['area'] = area
        context['region'] = region
        context['space_data'] = space
        bpy.data.objects['head_geo_rig'].select_set(False)
        bpy.data.objects['head_geo'].select_set(True)
        bpy.ops.view3d.view_selected(context)
        bpy.ops.view3d.view_axis(context, type='FRONT')
        context['space_data'].overlay.show_overlays = False

    def render_animation(self, output_path):
        self.set_frame_number()
        bpy.context.scene.render.filepath = output_path
        self.adjust_view()
        bpy.ops.render.opengl(animation=True)
        bpy.data.objects['head_geo_rig'].select_set(True)
        bpy.ops.object.delete(use_global=False)


    def import_fbx(self, file):
        bpy.ops.import_scene.fbx(filepath=file, global_scale=0.01) # bas
        bpy.context.selected_objects[0].name ='head_geo_rig'

           
        #Here we are Registering the Classes        
def register():
    bpy.utils.register_class(MAINUI)
    bpy.utils.register_class(WM_OT_batch_render)
    bpy.utils.register_class(WM_OT_batch_export_abc)
    bpy.utils.register_class(WM_OT_batch_render_bone_animation)
    
    #Here we are UnRegistering the Classes    
def unregister():
    bpy.utils.unregister_class(MAINUI)
    bpy.utils.unregister_class(WM_OT_batch_render)
    bpy.utils.unregister_class(WM_OT_batch_export_abc)
    bpy.utils.unregister_class(WM_OT_batch_render_bone_animation)
       
    #This is required in order for the script to run in the text editor    
if __name__ == "__main__":
    register()