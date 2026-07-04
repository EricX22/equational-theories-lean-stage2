% order5v2_0155  eq1=20935 eq2=23659  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Y),f(f(f(Z,Y),Z),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Z),X),f(Z,f(Z,X))) )).
