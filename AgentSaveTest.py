import Game
from Game import agents, encoders, nn

print('=== Agent Save and Load Test ===')

encoder = encoders.FourEncoder()
network = nn.SmallNetwork()
agent = agents.OpenAgent(encoder, network)

print('=== Save Agent ===')
file_name = 'AgentTest.h5'
agent.save(file_name)
print('Agent Saved')

print('=== Load Agent ===')
loaded_agent = agents.OpenAgent.load(file_name)

assert(agent.encoder.name() == loaded_agent.encoder.name())
assert(agent.network.name() == loaded_agent.network.name())
assert(agent.temperature == loaded_agent.temperature)
weight, loaded_weight = agent.nn_tsumo.get_weights(), loaded_agent.nn_tsumo.get_weights()
for layer, loaded_layer in zip(weight, loaded_weight):
    assert((layer == loaded_layer).all())
print('Agent Load Success')