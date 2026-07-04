% order5_0081  eq1=59577 eq2=19147  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(X,f(f(X,X),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,Y),f(f(Y,Z),f(Z,Y))) )).
