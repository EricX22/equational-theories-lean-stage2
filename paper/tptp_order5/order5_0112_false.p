% order5_0112  eq1=48288 eq2=51048  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(Z,f(Y,Z)),f(Y,X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,f(f(W,X),Z)),W) )).
