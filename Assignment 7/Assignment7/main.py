import csv

from neural import NeuralNet

# each row is an (input, output) tuple 
xor_data = [
    # input output corresponding example 
    ([0.0, 0.0], [0.0]), #[0, 0] => 0
    ([0.0, 1.0], [1.0]), #[0, 1] => 1 
    ([1.0, 0.0], [1.0]), #[1, 1] => 1 
    ([1.0, 1.0], [0.0])  #[1, 0] => 0
]
nn = NeuralNet(2, 1, 1)
nn.train(xor_data)

print(nn.evaluate([0.0, 1.0]))

for triple in nn.test_with_expected(xor_data): 
    print(triple)

for i in nn.test_with_expected(xor_data): 
    print(f"desired: {i[1]}, actual: {i[2]}")