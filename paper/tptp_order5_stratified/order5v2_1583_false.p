% order5v2_1583  eq1=5330 eq2=9300  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(W,f(X,Z))))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(X,X),f(Y,f(Z,Y)))) )).
