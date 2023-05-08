import random
import string

from Crypto.Hash import keccak

from itertools import combinations

def get_selector(signature):
  k = keccak.new(digest_bits=256)
  k.update(bytes(signature, 'utf-8'))
  return '0x' + k.hexdigest()[:8]

def generate_function(target_selector, args, function_name_len):
  letters = list(string.ascii_letters)
  letters.append('_')

  selector = ''
  candidate_char_indices = [0] * function_name_len
  next_candidate_char = 0

  for function_name_candidate in combinations(letters, function_name_len):
    print('trying: ' + ''.join(function_name_candidate))
    selector = get_selector(''.join(function_name_candidate) + args)
    print('gave me: ' + selector)
    if selector == target_selector:
      return { 'selector' : selector, 'function_signature' : ''.join(function_name_candidate) + args }

  return { 'selector' : 'NOT_FOUND' }

  # while selector != target_selector:
  #   candidate_function_name = ''
  #   for i in candidate_char_indices:
  #     candidate_function_name += letters[i]
  #   selector = get_selector(candidate_function_name + args)
  #   print('gave me: ' + selector)
  #   if selector == target_selector:
  #     return { 'selector' : selector, 'function_signature' : candidate_function_name + args }
  #   else:
  #     for i in candidate_char_indices:
  #       if i != len(letters) - 1:
  #         i += 1
  #         break
  #     if next_candidate_char == 0 and candidate_char_indices[-1] == len(letters) - 1:
  #       return { 'selector' : 'NOT_FOUND' }
  #     else:
  #       candidate_char_indices[next_candidate_char] += 1
  #       next_candidate_char = (next_candidate_char + 1) % len(candidate_char_indices)

def get_selector_collision(signature):
  function_name = signature[:signature.index('(')]
  function_args = signature[signature.index('('):]

  target_selector = get_selector(signature)
  print('target: ' + target_selector)

  max_function_name_len = 6
  candidate_function_length = 1

  returned_function = { 'selector' : 'NOT_FOUND', 'function_signature' : '' }
  while returned_function['selector'] != target_selector and candidate_function_length < max_function_name_len:
    returned_function = generate_function(target_selector, function_args, max_function_name_len)
    candidate_function_length += 1
  print('found: ' + str(returned_function))
