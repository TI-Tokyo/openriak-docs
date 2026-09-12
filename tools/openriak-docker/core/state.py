"""Persist phase progress independently from final image approval."""

def phase_for(name):
    if 'base_image' in name: return 'resolve'
    if name == 'build_image': return 'build'
    if 'artifact' in name: return 'generate'
    if 'export' in name or name == 'load_local_tags': return 'export'
    if 'remove_' in name: return 'cleanup'
    return 'test'


class StepReport(dict):
    def __init__(self, value, save):
        super().__init__(value)
        self.save = save

    def checkpoint(self):
        phases = {}
        for step in self.get('steps', []):
            phases.setdefault(phase_for(step['name']), []).append(step['status'])
        self['phases'] = {name: ('failed' if 'failed' in states else 'interrupted' if 'interrupted' in states else 'running' if 'running' in states else 'passed')
                          for name, states in phases.items()}
        self.save(self)
