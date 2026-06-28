% hard3_0269  eq1=2562 eq2=2100  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),W)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(Y,X),Y),f(Y,X)) )).
