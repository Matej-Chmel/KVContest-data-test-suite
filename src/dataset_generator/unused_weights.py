small.weights = [get_weights([2, 28, 1, 19, 48])]
# mH [('L', True), ('L', False), ('R', True), ('R', False), ('S', True), ('S', False), ('H',)]
medium_H.weights = [
    get_weights([0.2, 1.05, 0, 16.75, 75.65, 0.25]),
    get_weights([0.2, 1.05, 0, 12.15, 57.05, 0.25]),
    get_weights([0.2, 1.05, 0, 5.75, 20.75, 0.25])
]
# mAH [('L', True), ('L', False), ('R', True), ('R', False), ('S', True), ('S', False),
# ('A', True), ('A', False), ('H',)]
medium_AH.weights = [
    get_weights([0.05, 0.95, 0, 16.6, 75.5, 0.1, 0, 0.9]),
    get_weights([0.05, 0.95, 0, 12, 56.9, 0.1, 0, 0.9]),
    get_weights([0.05, 0.95, 0, 5.6, 20.5, 0.1, 0, 0.9])
]