import random
import string

from Crypto.Hash import keccak

from itertools import product

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

  for function_name_candidate in product(letters, repeat=function_name_len):
    print('trying: ' + ''.join(function_name_candidate))
    selector = get_selector(''.join(function_name_candidate) + args)
    print('gave me: ' + selector)
    if selector == target_selector:
      return { 'selector' : selector, 'function_signature' : ''.join(function_name_candidate) + args }

  return { 'selector' : 'NOT_FOUND' }

def get_selector_collision(signature):
  function_name = signature[:signature.index('(')]
  function_args = signature[signature.index('('):]

  target_selector = get_selector(signature)
  print('target: ' + target_selector)

  max_function_name_len = 2
  candidate_function_length = 1

  returned_function = { 'selector' : 'NOT_FOUND', 'function_signature' : '' }
  while returned_function['selector'] != target_selector and candidate_function_length < max_function_name_len:
    returned_function = generate_function(target_selector, function_args, max_function_name_len)
    candidate_function_length += 1
  print('found: ' + str(returned_function))
