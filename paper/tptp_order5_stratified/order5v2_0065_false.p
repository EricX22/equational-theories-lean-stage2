% order5v2_0065  eq1=1294 eq2=59469  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(X,Y),Z),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Y) != f(Y,f(f(X,Z),W)) )).
