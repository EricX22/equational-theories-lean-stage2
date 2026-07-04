% order5v2_1182  eq1=38464 eq2=58264  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(Y,Z),X)),W),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,X),Y) = f(X,f(Z,f(X,X))) )).
