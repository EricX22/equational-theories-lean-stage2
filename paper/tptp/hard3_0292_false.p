% hard3_0292  eq1=2757 eq2=835  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,Y)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(Y,X),f(Y,X))) )).
