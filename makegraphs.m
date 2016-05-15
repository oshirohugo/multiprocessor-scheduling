aux = dlmread('output-0.txt', ';');
generations = aux(:, 1);


best_fitness = [];

for i = 0:7
    filename = sprintf('complete-output-%d.txt', i);
    data = dlmread(filename, ';', 0, 1);
%     plot(generations, data)
%     hold on
    best_fitness = [best_fitness data];
end

best_fitness = best_fitness(1:50, :);

plot(best_fitness, 'LineWidth', 2)

legend(...
    'base config', ...
    'crossover technique = double point',...
    'mutation technique = seq swap',...
    'selection technique = roulette',...
    'substitution method = elitism',...
    'population size = 1000',...
    'crossover rate = 30%',...
    'mutation rate = 90%')

xlabel('generation')
ylabel('Average Fitness')
title('Average Fitness x generation')