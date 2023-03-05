% Run the simulation with the controller to test it

% First, run PENDULUM PARAMETERS box in pendulum.mlx

%% Params
sim_steps = 500;
dt = 0.01;
t = [0:dt:dt*(sim_steps-1)]';


%% Sim
% Resetting model to default
for i=1:19
    set_param(sprintf('pendulum_system_test/pendulum_links/pendulum_link_%d',i),'commented','off');
end

% Initialising number of links
for i=1:(20-n_links)
    set_param(sprintf('pendulum_system_test/pendulum_links/pendulum_link_%d',i),'commented','through');
end

test_simout = sim("pendulum_system_test.slx", t);