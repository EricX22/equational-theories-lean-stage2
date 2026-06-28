% hard3_0088  eq1=648 eq2=3869  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Z),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(X,f(Y,X)),Z) )).
