% order5v2_1212  eq1=22837 eq2=59577  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Y)),f(f(Y,X),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Z) != f(X,f(f(X,X),W)) )).
