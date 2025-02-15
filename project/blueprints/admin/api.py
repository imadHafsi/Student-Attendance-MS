from .head import *


@admin.route('/classes/get_classes_to_assign', methods=['POST'])
def get_classes_to_assign():
    data = request.get_json()
    my_id = data.get('id')  
    my_role = data.get('role')

    if my_role=='teacher':
        if not my_id:
            return jsonify({'error': 'Teacher ID is required'}), 400

        teacher = Teacher.query.filter_by(id=my_id).first()
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404

        all_classes = Class.query.all()  # Get all classes
        assigned_class_ids = {cls.id for cls in teacher.classes}  # Set of assigned class IDs

        teacher_classes = []
        for classe in all_classes:
            teacher_classes.append({
                'id': classe.id,
                'level': classe.level,
                'section': classe.section,
                'group': classe.group,
                'selected': classe.id in assigned_class_ids  # Check if class is assigned
            })

        return jsonify({'classes': teacher_classes})

    if my_role=='supervisor':
        if not my_id:
            return jsonify({'error': 'Supervisor ID is required'}), 400

        supervisor = Supervisor.query.filter_by(id=my_id).first()
        if not supervisor:
            return jsonify({'error': 'Supervisor not found'}), 404

        all_classes = Class.query.all()  # Get all classes
        assigned_class_ids = {cls.id for cls in supervisor.classes}  # Set of assigned class IDs

        supervisor_classes = []
        for classe in all_classes:
            supervisor_classes.append({
                'id': classe.id,
                'level': classe.level,
                'section': classe.section,
                'group': classe.group,
                'selected': classe.id in assigned_class_ids  # Check if class is assigned
            })

        return jsonify({'classes': supervisor_classes})
    
    return jsonify({'classes': [] })

@admin.route('/classes/get_sections', methods=['POST'])
def get_sections():
    data = request.get_json()
    level = data.get('level')

    if not level:
        return jsonify({'error': 'Level is required'}), 400

    sections = db.session.query(Class.section).filter_by(level=level).distinct().all()
    sections_list = [s[0] for s in sections]  # Extract section names

    return jsonify({'sections': sections_list})

@admin.route('/classes/get_groups', methods=['POST'])
def get_groups():
    data = request.get_json()
    level = data.get('level')
    section = data.get('section')

    if not level or not section:
        return jsonify({'error': 'Level and section are required'}), 400

    groups = db.session.query(Class.group).filter_by(level=level, section=section).distinct().all()
    groups_list = [g[0] for g in groups]  # Extract group values

    return jsonify({'groups': groups_list})