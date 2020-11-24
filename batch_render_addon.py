bl_info = {
    "name": "Batch Render",
    "author": "wangliyou",
    "version": (1, 1),
    "blender": (2, 83, 0),
    "location": "View3D > Toolbar > Batch Render",
    "description": "batch render video",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}
 
 
 
import bpy
import os
 
 
    #This is the Main Panel (Parent of Panel A and B)
class MainPanel(bpy.types.Panel):
    bl_label = "Batch Render"
    bl_idname = "VIEW_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Batch Render'
   
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text= "Batch Render", icon= 'OBJECT_ORIGIN')
        row = layout.row()
        row.operator("wm.batch_render", icon= 'CUBE', text= "batch_render")
 
 
class WM_OT_batch_render(bpy.types.Operator):
    """Open the Add Cube Dialog box"""
    bl_label = "Add Cube Dialog Box"
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
        for name in names:
            input_path = os.path.join(input_dir, name)
            self.import_fbx(input_path)
            output_path = os.path.join(output_dir, name[:-3]+'mp4')
            self.render_animation(output_path)
            print("-" * 100)
            print("{} render finish".format(name))
       
       
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
     
     
     
           
        #Here we are Registering the Classes        
def register():
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(WM_OT_batch_render)
   
   
 
    #Here we are UnRegistering the Classes    
def unregister():
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(WM_OT_batch_render)
       
    #This is required in order for the script to run in the text editor    
if __name__ == "__main__":
    register()