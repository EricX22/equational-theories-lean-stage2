% hard3_0171  eq1=1510 eq2=2140  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(W,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Y),Y),f(Z,X)) )).
