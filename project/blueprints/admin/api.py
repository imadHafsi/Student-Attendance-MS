from .head import *


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