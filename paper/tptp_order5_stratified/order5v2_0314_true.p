% order5v2_0314  eq1=35251 eq2=10373  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(f(W,X),X)),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Y,Y),f(f(Z,Y),Y))) )).
