% hard3_0209  eq1=1966 eq2=2207  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(Z,X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Z),Z),f(W,X)) )).
