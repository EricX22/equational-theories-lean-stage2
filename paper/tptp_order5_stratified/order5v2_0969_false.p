% order5v2_0969  eq1=40964 eq2=24764  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(f(Y,X),Z),Z),X),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Z),W),f(f(Y,Z),W)) )).
