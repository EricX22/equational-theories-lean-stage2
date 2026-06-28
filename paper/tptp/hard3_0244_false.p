% hard3_0244  eq1=2190 eq2=3388  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Y),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(Z,f(X,f(Z,Y))) )).
