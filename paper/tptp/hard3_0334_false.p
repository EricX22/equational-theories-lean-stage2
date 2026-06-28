% hard3_0334  eq1=3130 eq2=231  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,X),Z),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(Y,f(Y,Y)),X) )).
