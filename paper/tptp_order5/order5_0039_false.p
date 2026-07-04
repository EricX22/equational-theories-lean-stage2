% order5_0039  eq1=32934 eq2=36901  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(f(f(Y,Z),Z),W)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),Y),f(W,X)),Y) )).
