% hard3_0088  eq1=648 eq2=3869  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Z),W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(X,f(Y,X)),Z) )).
