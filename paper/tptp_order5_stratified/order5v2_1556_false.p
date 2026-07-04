% order5v2_1556  eq1=275 eq2=59542  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,X),Y),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Y) != f(Z,f(f(Z,Z),W)) )).
