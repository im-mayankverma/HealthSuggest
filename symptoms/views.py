from django.shortcuts import render
from .models import Symptom, ConditionSymptom


def home(request):
    symptoms = Symptom.objects.all()
    return render(request, 'symptoms/home.html', {'symptoms': symptoms})


def get_suggestions(request):
    if request.method == 'POST':
        selected_symptom_ids = request.POST.getlist('symptoms')
        duration_days_raw = request.POST.get('duration_days', '').strip()
        user_severity = request.POST.get('user_severity', 'mild')

        # Parse duration, default to 0 if blank/invalid
        try:
            duration_days = int(duration_days_raw) if duration_days_raw else 0
        except ValueError:
            duration_days = 0

        if not selected_symptom_ids:
            symptoms = Symptom.objects.all()
            return render(request, 'symptoms/home.html', {
                'symptoms': symptoms,
                'error': 'Please select at least one symptom.'
            })

        condition_scores = {}

        # Base scoring from symptom-condition weights
        for symptom_id in selected_symptom_ids:
            condition_symptoms = ConditionSymptom.objects.filter(symptom_id=symptom_id)
            for cs in condition_symptoms:
                if cs.condition.id not in condition_scores:
                    condition_scores[cs.condition.id] = {
                        'condition': cs.condition,
                        'score': 0,
                        'matched_symptoms': 0,
                        'total_symptoms': ConditionSymptom.objects.filter(condition=cs.condition).count(),
                    }
                condition_scores[cs.condition.id]['score'] += cs.weight
                condition_scores[cs.condition.id]['matched_symptoms'] += 1

        # Adjust scores based on user severity and duration
        severity_factor = {
            'mild': 1.0,
            'moderate': 1.1,
            'severe': 1.2,
        }.get(user_severity, 1.0)

        if duration_days >= 7:
            duration_factor = 1.2
        elif duration_days >= 3:
            duration_factor = 1.1
        else:
            duration_factor = 1.0

        results = []
        for _, data in condition_scores.items():
            if data['total_symptoms'] > 0:
                match_percentage = int((data['matched_symptoms'] / data['total_symptoms']) * 100)
            else:
                match_percentage = 0

            adjusted_score = data['score'] * severity_factor * duration_factor

            results.append({
                'condition': data['condition'],
                'match_percentage': match_percentage,
                'score': adjusted_score,
            })

        # Sort by match_percentage first, then by adjusted score
        results.sort(key=lambda x: (x['match_percentage'], x['score']), reverse=True)

        # Main best result
        best_result = results[0] if results else None

        # Other possible conditions (up to 3 others)
        other_results = results[1:4] if len(results) > 1 else []

        selected_symptoms = Symptom.objects.filter(id__in=selected_symptom_ids)

        # Compute a simple risk level from condition severity + match for the best result
        risk_level = None
        if best_result:
            cond_severity = best_result['condition'].severity
            match = best_result['match_percentage']

            if cond_severity == 'severe' or match >= 80:
                risk_level = 'high'
            elif cond_severity == 'moderate' or match >= 50:
                risk_level = 'medium'
            else:
                risk_level = 'low'

        return render(request, 'symptoms/results.html', {
            'best_result': best_result,
            'other_results': other_results,
            'selected_symptoms': selected_symptoms,
            'user_severity': user_severity,
            'duration_days': duration_days,
            'risk_level': risk_level,
        })

    symptoms = Symptom.objects.all()
    return render(request, 'symptoms/home.html', {'symptoms': symptoms})