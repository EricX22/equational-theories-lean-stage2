% order5v2_0111  eq1=29870 eq2=26335  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(Y,f(Z,X)))),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(f(Z,Y),X)),f(Z,Z)) )).
