import construct_words_json, math

def construct_frequency_array(candidate: str) -> list[int]:
	frequency = [0 for i in range(26)]
	for letter in candidate:
		frequency[ord(letter) - ord('a')] += 1
	return frequency

def construct_frequency_grid(candidates: list[str]) -> list[list[int]]:
	frequency_array = [[0 for i in range(26)] for j in range(len(candidates[0]))]
	for candidate in candidates:
		frequency = construct_frequency_array(candidate)
		for column in range(26):
			for row in range(frequency[column]):
				frequency_array[row][column] += 1
	return frequency_array

def construct_positional_frequency_grid(candidates: list[str]) -> list[list[int]]:
	positional_frequency_grid = [[0 for i in range(len(candidates[0]))] for j in range(26)]
	for candidate in candidates:
		for index in range(len(candidate)):
			positional_frequency_grid[ord(candidate[index]) - ord('a')][index] += 1
	return positional_frequency_grid

def get_similarity_value(frequency_grid: list[list[int]], candidate: str) -> int:
	similarity = 0
	frequency = construct_frequency_array(candidate)
	for column in range(26):
		for row in range(frequency[column]):
			similarity += frequency_grid[row][column]
	return similarity

def construct_similarity_array(candidates: list[str]) -> list[int]:
	frequency_grid = construct_frequency_grid(candidates)
	similarities = list()
	for candidate in candidates:
		similarities.append(get_similarity_value(frequency_grid, candidate))
	return similarities

def get_correct_value(positional_frequency_grid: list[list[int]], candidate: str) -> int:
	correct_value = 0
	for index in range(len(candidate)):
		correct_value += positional_frequency_grid[ord(candidate[index]) - ord('a')][index]
	return correct_value

def construct_correct_array(candidates: list[str]) -> list[int]:
	positional_frequency_grid = construct_positional_frequency_grid(candidates)
	correct = list()
	for candidate in candidates:
		correct.append(get_correct_value(positional_frequency_grid, candidate))
	return correct

def get_overall_score(similarity: int, correct: int) -> float:
	return similarity + correct * 1.0001

def value_candidates(candidates: list[str], popular_candidates: list[str]) -> dict[str,float]:
	naive_similarities = construct_similarity_array(candidates)
	correct_values = construct_correct_array(candidates)
	similarities = [naive_similarities[index] - correct_values[index] for index in range(len(naive_similarities))]
	for i in range(min(5, len(candidates))):
		print("Word: {}, Correct: {}, Similarity: {}".format(candidates[i], correct_values[i], similarities[i]))
	candidate_values = {}
	for index in range(len(candidates)):
		score = get_overall_score(similarities[index], correct_values[index])
		if candidates[index] in popular_candidates:
			score *= 2
		candidate_values[candidates[index]] = score
	return candidate_values

# When we guess a word, say apple, we can have character in the right spot,
# the wrong spot but still in the word, and not in the word at all.
# Denote these as C, S, and X respectively.
def guess_has_similarity_to_candidate(candidate: str, guess_score: str, guess: str) -> bool:
	if candidate == guess and 's' in guess_score:
		return False
	for index in range(len(guess_score)):
		if guess_score[index] == 's' and guess[index] == candidate[index]:
			return False
	guess_score = str.lower(guess_score)
	correct_indices = list()
	for index in range(len(guess)):
		if guess_score[index] == 'c':
			if candidate[index] != guess[index]:
				return False
			else:
				correct_indices.append(index)
	candidate = ''.join([candidate[i] for i in range(len(candidate)) if i not in correct_indices])

	for index in range(len(guess)):
		if guess_score[index] == 's':
			if guess[index] not in candidate:
				return False
			else:
				candidate = candidate.replace(guess[index], '', 1)
		if guess_score[index] == 'x':
			if guess[index] in candidate:
				return False
	return True
	
def generate_guess_score(guess: str, answer: str) -> str:
	if len(answer) == 0:
		return input('Input how the word did. C for correct, S for similar, X for not present\n')
	answer_array = list(answer)
	guess_score = [''] * len(guess)
	for index in range(len(guess)):
		if guess[index] == answer_array[index]:
			guess_score[index] = 'c'
			answer_array[index] = ' '
	for index in range(len(guess)):
		if guess_score[index] == 'c':
			continue
		if guess[index] in answer_array:
			guess_score[index] = 's'
			answer_array[answer_array.index(guess[index])] = ' '
		else:
			guess_score[index] = 'x'
	answer = ''.join(guess_score)
	print(answer)
	return answer

def simulate_game(candidates: list[str], popular_candidates: list[str], answer: str = '') -> int:
	answer = answer.lower()
	guesses = 0
	while len(candidates) > 1:
		guesses += 1
		print(len(candidates))
		candidate_values = value_candidates(candidates, popular_candidates)
		max_value = -100000000000
		max_word = "asdf"
		for key in candidate_values.keys():
			value = candidate_values[key]
			if value > max_value:
				max_value = value
				max_word = key
		print("Best candidate: {} with a score of {}".format(max_word, max_value))
		if (max_word == answer):
			guesses -= 1
		guess_score = generate_guess_score(max_word, answer)
		candidates = list(filter(lambda candidate: guess_has_similarity_to_candidate(candidate, guess_score, max_word), candidates))
		popular_candidates = list(filter(lambda candidate: guess_has_similarity_to_candidate(candidate, guess_score, max_word), popular_candidates))

	if len(candidates) == 0 or (answer != '' and candidates[0] != answer):
		print("The word {} isn't present in the dictionary".format(answer))
	else:
		print("Answer: {} in {} guesses".format(candidates[0], guesses + 1))
	return guesses + 1

if __name__ == '__main__':
	words_dict: dict = construct_words_json.get_dict_from_all_file()
	popular_words_dict: dict = construct_words_json.get_dict_from_popular_file()
	answer = 'boost'
	length = len(answer)
	if length == 0:
		length = int(input('Input the length of the word\n'))
	candidates = words_dict[str(length)]
	popular_candidates = popular_words_dict[str(length)]
	simulate_game(candidates, popular_candidates, answer=answer)
