% hard3_0321  eq1=2985 eq2=1374  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,X)),W),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(Z,Y),Z),X)) )).
