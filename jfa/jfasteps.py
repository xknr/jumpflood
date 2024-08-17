class JfaSteps:

    def calcMaxStep(w, h):
        assert w > 0 and h > 0
        return max(w, h)
 
    def jfaIncreasing(w, h):
        maxStep = JfaSteps.calcMaxStep(w, h)
        steps = []

        step = 1
        while step < maxStep:
            steps.append(step)
            step *= 2

        return steps
    def jfa(w, h):
        maxStep = JfaSteps.calcMaxStep(w, h)
        steps = []

        step = 1
        while step * 2 < maxStep:
            step *= 2

        while step > 0:
            steps.append(step)
            step //= 2

        return steps

    def _1jfa(w, h):
        steps = JfaSteps.jfa(w, h)
        steps.insert(0, 1)
        return steps

    def jfa1(w, h):
        steps = JfaSteps.jfa(w, h)
        steps.append(1)
        return steps

    def jfa2(w, h):
        steps = JfaSteps.jfa(w, h)
        steps.append(2)
        steps.append(1)
        return steps

    def jfaPow2(w, h):
        steps = JfaSteps.jfa(w, h)
        steps = steps * 2
        return steps
    

