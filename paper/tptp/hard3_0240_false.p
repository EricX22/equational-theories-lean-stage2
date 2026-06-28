% hard3_0240  eq1=2156 eq2=2097  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(Y,X),Y),f(X,X)) )).
